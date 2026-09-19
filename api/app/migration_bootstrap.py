"""Migration bootstrap — safely bring legacy databases under Alembic control.

Handles these database states:

  State 1 — Fresh:
    bookings absent, alembic_version absent or empty
    → alembic upgrade head

  State 2 — Supported legacy:
    bookings exists, alembic_version absent or empty
    → validate schema matches 0001, stamp 0001, upgrade head

  State 3 — Already managed:
    alembic_version contains a valid revision
    → verify no future-revision tables already exist (inconsistent stamp),
      then alembic upgrade head (no stamp, no reset)

  State 4 — Unsafe:
    bookings schema incompatible, corrupt revision table, an inconsistent
    stamp (alembic_version behind tables that already exist), or any other
    inconsistent state
    → fail closed with non-zero exit, log diagnostic

Usage:
    python -m app.migration_bootstrap
"""

import logging
import sys
from typing import Optional

from alembic import command
from alembic.config import Config
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import get_settings
from app.core.database import _get_engine

logger = logging.getLogger("migration_bootstrap")


class BootstrapError(Exception):
    """Raised when the migration bootstrap fails (unsafe state)."""

    def __init__(self, reason: str):
        super().__init__(reason)


# ---------------------------------------------------------------------------
# Schema expected by migration 0001 for the bookings table.
# (column_name, type_substrings, nullable)
# type_substrings are checked case-insensitively — at least one must be
# found in the dialect-reported type string. PostgreSQL reports
# "CHARACTER VARYING" and "TIMESTAMP WITH TIME ZONE".
# ---------------------------------------------------------------------------
BOOKINGS_0001_COLUMNS = [
    ("id", ("INTEGER",), False),
    ("service_type", ("VARCHAR", "CHARACTER VARYING"), False),
    ("visit_type", ("VARCHAR", "CHARACTER VARYING"), False),
    ("preferred_day", ("VARCHAR", "CHARACTER VARYING"), False),
    ("preferred_time", ("VARCHAR", "CHARACTER VARYING"), False),
    ("time_window", ("VARCHAR", "CHARACTER VARYING"), True),
    ("first_name", ("VARCHAR", "CHARACTER VARYING"), False),
    ("last_name", ("VARCHAR", "CHARACTER VARYING"), False),
    ("email", ("VARCHAR", "CHARACTER VARYING"), False),
    ("phone", ("VARCHAR", "CHARACTER VARYING"), False),
    ("reason_category", ("VARCHAR", "CHARACTER VARYING"), False),
    ("status", ("VARCHAR", "CHARACTER VARYING"), False),
    ("created_at", ("DATETIME", "TIMESTAMP"), False),
]


# ---------------------------------------------------------------------------
# Sentinel tables introduced by each migration AFTER 0001. Used in State 3 to
# detect an inconsistent stamp: if alembic_version is at revision R but a table
# introduced by a later revision already exists, the DB is in the broken state
# we recovered from once (0002 tables present while stamped at 0001). Running
# `upgrade` in that state crashes with "relation already exists"; instead we
# fail closed with a clear, actionable message.
#
# Map: revision that MUST already be applied  ->  a table that revision creates.
# If the DB is stamped BELOW `revision` but the sentinel table exists, that is
# an inconsistent stamp.
# ---------------------------------------------------------------------------
REVISION_SENTINEL_TABLES = {
    "0002": "services",
    "0003": "patient_registrations",
}

# Ordered list of known revisions, oldest first. Used to compare positions.
REVISION_ORDER = ["0001", "0002", "0003"]


def _get_alembic_config() -> Config:
    """Load Alembic configuration, overriding the database URL from settings."""
    config = Config("alembic.ini")
    settings = get_settings()
    url = settings.effective_database_url
    if url:
        config.set_main_option("sqlalchemy.url", url)
    return config


def _table_exists(conn, table_name: str) -> bool:
    return table_name in inspect(conn).get_table_names()


def _count_version_rows(conn) -> int:
    """Return the number of rows in alembic_version (0 if absent)."""
    if not _table_exists(conn, "alembic_version"):
        return 0
    result = conn.execute(text("SELECT COUNT(*) FROM alembic_version"))
    return result.scalar()


def _get_current_revision(conn) -> Optional[str]:
    """Return the single Alembic revision, or None if unversioned/corrupt."""
    if not _table_exists(conn, "alembic_version"):
        return None
    try:
        result = conn.execute(
            text("SELECT version_num FROM alembic_version")
        )
        rows = result.fetchall()
        if len(rows) == 0:
            return None
        if len(rows) == 1:
            return rows[0][0]
        # Multiple rows — corrupt.
        logger.error(
            "alembic_version contains %d rows (expected 0 or 1).", len(rows)
        )
        return None
    except SQLAlchemyError:
        return None


def _revision_index(revision: Optional[str]) -> int:
    """Return the position of a revision in REVISION_ORDER, or -1 if unknown.

    An unknown revision returns a sentinel of -1 so callers can treat it as
    'not comparable' rather than silently mis-ordering.
    """
    if revision is None:
        return -1
    try:
        return REVISION_ORDER.index(revision)
    except ValueError:
        return -1


def _detect_inconsistent_stamp(conn, current_rev: str) -> Optional[str]:
    """Detect a stamp that is behind tables that already exist.

    For each revision whose sentinel table exists in the DB, if the current
    stamp is BELOW that revision, the database is inconsistent: a later
    migration's tables are present but alembic_version was never advanced.
    Returns a human-readable reason, or None if consistent.
    """
    current_idx = _revision_index(current_rev)

    for revision, sentinel_table in REVISION_SENTINEL_TABLES.items():
        if not _table_exists(conn, sentinel_table):
            continue
        rev_idx = _revision_index(revision)
        # If the sentinel table exists but the stamp is below the revision that
        # creates it (or the stamp is an unknown revision), that's inconsistent.
        if current_idx < rev_idx:
            return (
                f"inconsistent Alembic state: table '{sentinel_table}' "
                f"(introduced by revision {revision}) already exists, but "
                f"alembic_version is stamped at '{current_rev}', which is "
                f"before {revision}. A previous migration left tables behind "
                f"without advancing the revision. Running 'upgrade' would fail "
                f"with 'relation already exists'. Manual intervention required: "
                f"drop the orphaned tables from revision {revision} (if empty) "
                f"so the upgrade can re-run, or stamp the correct revision after "
                f"verifying the schema. Do not destroy data tables (e.g. bookings)."
            )

    return None


def _validate_bookings_schema(conn) -> bool:
    """Check that the existing bookings table matches migration 0001.

    Returns True if compatible, False if any required column is missing
    or has an incompatible definition.
    """
    inspector = inspect(conn)
    columns = {c["name"]: c for c in inspector.get_columns("bookings")}

    for col_name, type_substrs, nullable in BOOKINGS_0001_COLUMNS:
        if col_name not in columns:
            logger.error(
                "Required column '%s' is missing from bookings.", col_name
            )
            return False

        actual = columns[col_name]
        if actual["nullable"] != nullable:
            logger.error(
                "Column '%s' nullable mismatch: expected=%s actual=%s.",
                col_name, nullable, actual["nullable"],
            )
            return False

        actual_type = str(actual["type"]).upper()
        if not any(ts.upper() in actual_type for ts in type_substrs):
            logger.error(
                "Column '%s' type mismatch: expected one of %s, got '%s'.",
                col_name, type_substrs, actual_type,
            )
            return False

    # Verify primary key includes id.
    pk = inspector.get_pk_constraint("bookings")
    pk_cols = pk.get("constrained_columns", [])
    if "id" not in pk_cols:
        logger.error("bookings primary key does not include 'id'.")
        return False

    return True


def _fail(reason: str) -> None:
    """Raise BootstrapError — caller decides exit behaviour."""
    raise BootstrapError(reason)


def main() -> None:
    """Run the migration bootstrap state machine."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s [%(name)s] %(message)s",
    )

    config = _get_alembic_config()
    engine = _get_engine()

    # ------------------------------------------------------------------
    # Inspect current database state in a single short-lived connection.
    # ------------------------------------------------------------------
    with engine.connect() as conn:
        bookings_exists = _table_exists(conn, "bookings")
        version_rows = _count_version_rows(conn)
        current_rev = _get_current_revision(conn)

    # ------------------------------------------------------------------
    # State 4 detection — malformed revision table.
    # ------------------------------------------------------------------
    if version_rows > 1:
        _fail(
            f"alembic_version contains {version_rows} rows "
            f"(expected 0 or 1); manual intervention required"
        )

    # ------------------------------------------------------------------
    # State 3 — Already managed.
    # ------------------------------------------------------------------
    if current_rev is not None and version_rows == 1:
        # Guard against an inconsistent stamp (alembic_version behind tables
        # that already exist) before attempting an upgrade that would crash.
        with engine.connect() as conn:
            inconsistent = _detect_inconsistent_stamp(conn, current_rev)
        if inconsistent is not None:
            _fail(inconsistent)

        logger.info(
            "Database already managed by Alembic (revision %s). "
            "Running upgrade to head.",
            current_rev,
        )
        command.upgrade(config, "head")
        logger.info("Upgrade complete.")
        return

    # ------------------------------------------------------------------
    # State 2 — Legacy database (bookings exists, unversioned).
    # ------------------------------------------------------------------
    if bookings_exists:
        logger.info(
            "Legacy database: bookings table exists, Alembic not initialized."
        )

        # Validate the schema matches migration 0001.
        with engine.connect() as conn:
            valid = _validate_bookings_schema(conn)

        if not valid:
            _fail("bookings schema is incompatible with migration 0001")

        logger.info("bookings schema validated — matches migration 0001.")

        # A legacy DB must not already contain later-revision tables. If it
        # does, this is the inconsistent-stamp state (without a stamp yet):
        # fail closed rather than stamping 0001 and then crashing on upgrade.
        with engine.connect() as conn:
            for revision, sentinel_table in REVISION_SENTINEL_TABLES.items():
                if _table_exists(conn, sentinel_table):
                    _fail(
                        f"legacy database also contains table "
                        f"'{sentinel_table}' from revision {revision}; this is "
                        f"an inconsistent state. Expected only the legacy "
                        f"bookings table. Manual intervention required: drop the "
                        f"orphaned revision {revision} tables (if empty) before "
                        f"re-running the bootstrap."
                    )

        # Stamp revision 0001 so Alembic knows this migration ran.
        logger.info("Stamping revision 0001 (bookings table already exists).")
        command.stamp(config, "0001")

        # Apply remaining migrations (0002+).
        logger.info("Running upgrade to head.")
        command.upgrade(config, "head")
        logger.info("Bootstrap complete — legacy database now managed by Alembic.")
        return

    # ------------------------------------------------------------------
    # State 4 — bookings absent but version table has rows (no valid rev).
    # ------------------------------------------------------------------
    if version_rows > 0 and current_rev is None:
        _fail(
            "alembic_version table exists with rows but no valid revision "
            "could be read; manual intervention required"
        )

    # ------------------------------------------------------------------
    # A previous failed attempt may have created an empty alembic_version
    # table. This is still treated as State 1 (fresh) — but only if no
    # later-revision tables are lying around.
    # ------------------------------------------------------------------
    if not bookings_exists and version_rows == 0:
        with engine.connect() as conn:
            for revision, sentinel_table in REVISION_SENTINEL_TABLES.items():
                if _table_exists(conn, sentinel_table):
                    _fail(
                        f"database has no bookings table and no revision, but "
                        f"table '{sentinel_table}' from revision {revision} "
                        f"exists; inconsistent state. Manual intervention "
                        f"required before bootstrap can proceed."
                    )

        logger.info("Fresh database — running all migrations from scratch.")
        command.upgrade(config, "head")
        logger.info("Bootstrap complete — fresh database created.")
        return

    # ------------------------------------------------------------------
    # State 4 — Catch-all for any unexpected combination.
    # ------------------------------------------------------------------
    _fail("unexpected database state — cannot determine safe migration path")


def _run() -> None:
    """Entry point with top-level error handling."""
    try:
        main()
    except BootstrapError as exc:
        logger.error("Bootstrap failed: %s", exc)
        sys.exit(1)
    except Exception:
        logger.exception("Bootstrap failed with unexpected error")
        sys.exit(2)


if __name__ == "__main__":
    _run()
