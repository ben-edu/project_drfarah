"""Regression coverage retained while the migration head moves to 0004."""

import os

import pytest
from sqlalchemy import create_engine, text

from tests.test_migration_bootstrap import (
    _count_rows,
    _create_legacy_bookings_table,
    _get_revision,
    _insert_legacy_bookings,
    _run_bootstrap,
    _stamp,
    pg_db,
)

pytestmark = pytest.mark.postgresql


def test_fresh_bootstrap_preserves_seed_services_and_hours(pg_db):
    _run_bootstrap()
    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        service_codes = {
            row[0]
            for row in conn.execute(text("SELECT code FROM services ORDER BY code")).fetchall()
        }
        hours_count = conn.execute(text("SELECT COUNT(*) FROM working_hours")).scalar()
    engine.dispose()

    assert service_codes == {"rejuvenation", "traveler-care", "urgent-care", "vip-mobile"}
    assert hours_count == 5


def test_legacy_booking_ids_survive_upgrade(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=3)

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        before = [row[0] for row in conn.execute(text("SELECT id FROM bookings ORDER BY id"))]
    engine.dispose()

    _run_bootstrap()

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        after = [row[0] for row in conn.execute(text("SELECT id FROM bookings ORDER BY id"))]
    engine.dispose()

    assert before == after
    assert _count_rows(db_url, "bookings") == 3


def test_unversioned_legacy_with_orphan_0002_table_fails_before_stamp(pg_db):
    from app.migration_bootstrap import BootstrapError

    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=1)

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE services (id SERIAL PRIMARY KEY, code VARCHAR(64) UNIQUE NOT NULL)"
        ))
    engine.dispose()

    with pytest.raises(BootstrapError) as excinfo:
        _run_bootstrap()

    assert "inconsistent" in str(excinfo.value).lower()
    assert _get_revision(db_url) is None
    assert _count_rows(db_url, "bookings") == 1


def test_inconsistent_stamp_top_level_exit_code_remains_one(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=1)
    _stamp(db_url, "0001")

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE services (id SERIAL PRIMARY KEY, code VARCHAR(64) UNIQUE NOT NULL)"
        ))
    engine.dispose()

    from app import migration_bootstrap
    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SMTP_TEST_MODE"] = "true"
    os.environ["CLEANUP_TOKEN"] = "test-token"

    with pytest.raises(SystemExit) as excinfo:
        migration_bootstrap._run()
    assert excinfo.value.code == 1
