"""Integration tests for migration bootstrap against disposable PostgreSQL databases.

Each test creates a unique temporary PostgreSQL database, constructs the
required schema state, runs the bootstrap, and verifies the result.

Databases are created via sudo -u postgres and dropped after each test.
"""

import datetime
import os
import re
import subprocess
import sys
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

CLINIC_TZ = ZoneInfo("America/Los_Angeles")

# ---------------------------------------------------------------------------
# Helpers — temporary PostgreSQL database management.
# ---------------------------------------------------------------------------

_TEST_DB_PREFIX = "drfarah_migration_test_"


def _run_psql(sql: str) -> None:
    """Execute a SQL command against the test database."""
    db_url = os.environ.get("DATABASE_URL", "")
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        conn.execute(text(sql))
        conn.commit()
    engine.dispose()


def _create_test_db(db_name: str) -> None:
    subprocess.run(
        ["sudo", "-u", "postgres", "createdb", "-O", "ben", db_name],
        check=True,
    )


def _drop_test_db(db_name: str) -> None:
    # Terminate any lingering connections before dropping.
    subprocess.run(
        [
            "sudo", "-u", "postgres", "psql", "-c",
            f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
            f"FROM pg_stat_activity "
            f"WHERE pg_stat_activity.datname = '{db_name}' "
            f"AND pid <> pg_backend_pid()",
        ],
        check=False,
        capture_output=True,
    )
    subprocess.run(
        ["sudo", "-u", "postgres", "dropdb", "--if-exists", db_name],
        check=True,
    )


def _table_exists(db_url: str, table_name: str) -> bool:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        result = table_name in inspect(conn).get_table_names()
    engine.dispose()
    return result


def _version_rows(db_url: str) -> int:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        if "alembic_version" not in inspect(conn).get_table_names():
            engine.dispose()
            return 0
        result = conn.execute(text("SELECT COUNT(*) FROM alembic_version"))
        count = result.scalar()
    engine.dispose()
    return count


def _get_revision(db_url: str) -> str | None:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        if "alembic_version" not in inspect(conn).get_table_names():
            engine.dispose()
            return None
        result = conn.execute(text("SELECT version_num FROM alembic_version"))
        rows = result.fetchall()
    engine.dispose()
    if len(rows) == 0:
        return None
    return rows[0][0]


def _count_rows(db_url: str, table_name: str) -> int:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        count = result.scalar()
    engine.dispose()
    return count


def _run_bootstrap() -> None:
    """Import and run the bootstrap.  Raises on failure."""
    os.environ["SMTP_HOST"] = ""
    os.environ["SMTP_TEST_MODE"] = "true"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["CLEANUP_TOKEN"] = "test-token"

    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()

    from app.migration_bootstrap import main

    main()


# ---------------------------------------------------------------------------
# Database fixtures — each test gets its own disposable PostgreSQL database.
# ---------------------------------------------------------------------------


@pytest.fixture
def pg_db(request):
    """Create a unique disposable PostgreSQL database.

    Cleanup runs even if the test fails.
    """
    test_name = re.sub(
        r"[^a-z0-9_]",
        "",
        request.node.name.replace(" ", "_").lower(),
    )
    db_name = f"{_TEST_DB_PREFIX}{test_name}"

    # Ensure no leftover from a previous interrupted run.
    _drop_test_db(db_name)

    _create_test_db(db_name)

    # Set the environment so the bootstrap uses this database.
    db_url = f"postgresql:///{db_name}?host=/var/run/postgresql"
    os.environ["DATABASE_URL"] = db_url

    yield db_name

    # Close all connections so we can drop the database.
    from app.core.database import reset_engine
    reset_engine()

    _drop_test_db(db_name)

    os.environ.pop("DATABASE_URL", None)

    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()


def _legacy_booking_row(index: int):
    """Return values for a representative legacy booking (matching 0001 schema)."""
    return {
        "service_type": "Urgent or acute care",
        "visit_type": "Clinic visit",
        "preferred_day": f"Monday {index}",
        "preferred_time": f"{8 + index}:00 AM",
        "time_window": "Morning",
        "first_name": f"Legacy{index}",
        "last_name": f"Patient{index}",
        "email": f"legacy{index}@example.com",
        "phone": f"+1-555-{index:04d}",
        "reason_category": "General appointment request",
    }


def _create_legacy_bookings_table(db_url: str) -> None:
    """Create a bookings table matching the application's original schema (0001)."""
    from sqlalchemy import (
        Column, DateTime, Integer, String, Text, func,
    )
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class LegacyBooking(Base):
        __tablename__ = "bookings"
        id = Column(Integer, primary_key=True, index=True)
        service_type = Column(String(128), nullable=False)
        visit_type = Column(String(128), nullable=False)
        preferred_day = Column(String(64), nullable=False)
        preferred_time = Column(String(32), nullable=False)
        time_window = Column(String(64), nullable=True)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        email = Column(String(255), nullable=False)
        phone = Column(String(64), nullable=False)
        reason_category = Column(String(128), nullable=False)
        status = Column(
            String(32), nullable=False, server_default="requested",
        )
        created_at = Column(
            DateTime(timezone=True), server_default=func.now(), nullable=False,
        )

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    Base.metadata.create_all(bind=engine, tables=[LegacyBooking.__table__])
    engine.dispose()


def _insert_legacy_bookings(db_url: str, count: int = 3) -> list[dict]:
    """Insert representative legacy booking rows."""
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    rows = []
    for i in range(1, count + 1):
        values = _legacy_booking_row(i)
        row = text(
            "INSERT INTO bookings (service_type, visit_type, preferred_day, "
            "preferred_time, time_window, first_name, last_name, email, phone, "
            "reason_category) "
            "VALUES (:service_type, :visit_type, :preferred_day, "
            ":preferred_time, :time_window, :first_name, :last_name, :email, "
            ":phone, :reason_category)"
        )
        db.execute(row, values)
        rows.append(values)
    db.commit()
    db.close()
    engine.dispose()
    return rows


def _create_empty_alembic_version(db_url: str) -> None:
    """Create an empty alembic_version table (simulating a failed attempt)."""
    from sqlalchemy import Column, String
    from sqlalchemy.orm import declarative_base

    Base = declarative_base()

    class AlembicVersion(Base):
        __tablename__ = "alembic_version"
        version_num = Column(String(32), primary_key=True)

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    Base.metadata.create_all(bind=engine, tables=[AlembicVersion.__table__])
    engine.dispose()


# ===========================================================================
# Tests
# ===========================================================================


class TestFreshDatabase:
    """State 1 — Empty database, nothing exists."""

    def test_bootstrap_creates_all_tables(self, pg_db):
        _run_bootstrap()

        db_url = os.environ["DATABASE_URL"]
        for table in ("bookings", "services", "working_hours",
                       "blocked_periods", "appointments", "alembic_version"):
            assert _table_exists(db_url, table), f"Table '{table}' is missing"

    def test_seed_services_exist(self, pg_db):
        _run_bootstrap()

        db_url = os.environ["DATABASE_URL"]
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT code, name, duration_minutes FROM services "
                     "ORDER BY code")
            )
            rows = result.fetchall()
        engine.dispose()
        codes = {row[0] for row in rows}
        assert codes == {"rejuvenation", "traveler-care", "urgent-care", "vip-mobile"}

    def test_seed_working_hours_exist(self, pg_db):
        _run_bootstrap()

        db_url = os.environ["DATABASE_URL"]
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT COUNT(*) FROM working_hours")
            )
            count = result.scalar()
        engine.dispose()
        assert count == 5  # Mon-Fri

    def test_alembic_reaches_head(self, pg_db):
        _run_bootstrap()

        db_url = os.environ["DATABASE_URL"]
        rev = _get_revision(db_url)
        assert rev is not None, "alembic_version should contain a revision"
        assert rev == "0002", f"Expected head 0002, got {rev}"

    def test_second_bootstrap_is_idempotent(self, pg_db):
        _run_bootstrap()
        # Second run should succeed without error.
        _run_bootstrap()

        db_url = os.environ["DATABASE_URL"]
        assert _get_revision(db_url) == "0002"


class TestLegacyDatabase:
    """State 2 — bookings exists, unversioned, schema is compatible."""

    @pytest.fixture(autouse=True)
    def setup_legacy(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        _create_legacy_bookings_table(db_url)

    def test_legacy_bookings_table_stamped_and_upgraded(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        _insert_legacy_bookings(db_url, count=2)

        # Verify no alembic_version before bootstrap.
        assert not _table_exists(db_url, "alembic_version")

        _run_bootstrap()

        # alembic_version should exist with revision at head.
        assert _get_revision(db_url) == "0002"

        # bookings table should still exist.
        assert _table_exists(db_url, "bookings")

        # Scheduling tables should now exist.
        for table in ("services", "working_hours", "blocked_periods", "appointments"):
            assert _table_exists(db_url, table), f"'{table}' missing"

    def test_legacy_rows_preserved(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        inserted = _insert_legacy_bookings(db_url, count=3)

        _run_bootstrap()

        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT first_name, last_name, email, reason_category "
                     "FROM bookings ORDER BY id")
            )
            rows = result.fetchall()
        engine.dispose()

        assert len(rows) == 3
        for i, row in enumerate(rows):
            expected = inserted[i]
            assert row[0] == expected["first_name"]
            assert row[1] == expected["last_name"]
            assert row[2] == expected["email"]
            assert row[3] == expected["reason_category"]

    def test_bookings_not_recreated(self, pg_db):
        """Prove bookings is not dropped/recreated — row IDs are preserved."""
        db_url = os.environ["DATABASE_URL"]
        _insert_legacy_bookings(db_url, count=1)

        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM bookings"))
            original_ids = [r[0] for r in result.fetchall()]
        engine.dispose()

        _run_bootstrap()

        engine = create_engine(db_url, connect_args={"connect_timeout": 5})
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM bookings"))
            after_ids = [r[0] for r in result.fetchall()]
        engine.dispose()

        assert original_ids == after_ids, "Booking IDs changed — table may have been recreated"

    def test_second_bootstrap_idempotent(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        _insert_legacy_bookings(db_url, count=1)
        _run_bootstrap()
        # Second run should succeed.
        _run_bootstrap()
        assert _get_revision(db_url) == "0002"


class TestEmptyAlembicVersion:
    """booksings + empty alembic_version → treated as legacy (State 2)."""

    @pytest.fixture(autouse=True)
    def setup_empty_version(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        _create_legacy_bookings_table(db_url)
        _insert_legacy_bookings(db_url, count=1)
        _create_empty_alembic_version(db_url)

    def test_succeeds_as_legacy(self, pg_db):
        db_url = os.environ["DATABASE_URL"]
        assert _version_rows(db_url) == 0
        assert _table_exists(db_url, "bookings")

        _run_bootstrap()

        assert _get_revision(db_url) == "0002"
        assert _count_rows(db_url, "bookings") == 1


class TestUnsafeIncompatibleSchema:
    """State 4 — bookings exists but schema is incompatible."""

    def test_missing_required_column_rejected(self, pg_db):
        """Create bookings without the 'reason_category' column."""
        db_url = os.environ["DATABASE_URL"]
        engine = create_engine(db_url, connect_args={"connect_timeout": 5})

        # Create bookings with a missing required column.
        from sqlalchemy import Column, DateTime, Integer, String, func
        from sqlalchemy.orm import declarative_base

        Base = declarative_base()

        class BadBooking(Base):
            __tablename__ = "bookings"
            id = Column(Integer, primary_key=True, index=True)
            service_type = Column(String(128), nullable=False)
            visit_type = Column(String(128), nullable=False)
            preferred_day = Column(String(64), nullable=False)
            preferred_time = Column(String(32), nullable=False)
            # time_window omitted intentionally (it's optional, should be fine)
            first_name = Column(String(128), nullable=False)
            last_name = Column(String(128), nullable=False)
            email = Column(String(255), nullable=False)
            phone = Column(String(64), nullable=False)
            # reason_category INTENTIONALLY MISSING — required column is absent.
            status = Column(String(32), nullable=False, server_default="requested")
            created_at = Column(
                DateTime(timezone=True), server_default=func.now(), nullable=False,
            )

        Base.metadata.create_all(bind=engine, tables=[BadBooking.__table__])
        engine.dispose()

        with pytest.raises(Exception):
            _run_bootstrap()

        # Verify no stamp occurred.
        assert _version_rows(db_url) == 0
        assert _get_revision(db_url) is None

        # Booking table and rows should still exist.
        assert _table_exists(db_url, "bookings")


class TestAlreadyManaged:
    """State 3 — alembic_version has a valid revision."""

    def test_upgrades_from_0001_to_head(self, pg_db):
        db_url = os.environ["DATABASE_URL"]

        # Create the legacy bookings table first.
        _create_legacy_bookings_table(db_url)
        _insert_legacy_bookings(db_url, count=1)

        # Run Alembic directly to stamp and run migration.
        from alembic import command
        from alembic.config import Config
        from app.core.config import get_settings
        from app.core.database import reset_engine

        get_settings.cache_clear()
        reset_engine()
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", db_url)

        # Stamp to 0001 (simulating a managed database at 0001).
        command.stamp(cfg, "0001")

        assert _get_revision(db_url) == "0001"

        # Now run the bootstrap — it should upgrade from 0001 to head.
        _run_bootstrap()

        assert _get_revision(db_url) == "0002"
        assert _table_exists(db_url, "services")
        assert _table_exists(db_url, "working_hours")
        # Existing data should be preserved.
        assert _count_rows(db_url, "bookings") == 1

    def test_already_at_head_passes(self, pg_db):
        db_url = os.environ["DATABASE_URL"]

        _create_legacy_bookings_table(db_url)
        _insert_legacy_bookings(db_url, count=1)

        from alembic import command
        from alembic.config import Config
        from app.core.config import get_settings
        from app.core.database import reset_engine

        get_settings.cache_clear()
        reset_engine()
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", db_url)
        command.stamp(cfg, "0001")
        command.upgrade(cfg, "head")

        assert _get_revision(db_url) == "0002"

        # Bootstrap should be a no-op.
        _run_bootstrap()
        assert _get_revision(db_url) == "0002"
        assert _count_rows(db_url, "bookings") == 1
