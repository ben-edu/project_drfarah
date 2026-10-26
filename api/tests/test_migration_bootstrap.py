"""Integration tests for the fail-closed migration bootstrap.

The tests use disposable PostgreSQL databases supplied by CI through
POSTGRES_TEST_DATABASE_URL. They cover fresh, legacy, managed, and inconsistent
states and assert that the current Alembic head is reached without losing data.
"""

import os

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

from tests._pg_util import (
    create_db,
    maintenance_url,
    per_test_db_url,
    terminate_and_drop,
    unique_db_name,
)

pytestmark = pytest.mark.postgresql

_TEST_DB_PREFIX = "drfarah_migration_test_"
EXPECTED_HEAD = "0004"
EXPECTED_TABLES = {
    "bookings",
    "services",
    "working_hours",
    "blocked_periods",
    "appointments",
    "patient_registrations",
    "appointment_attributions",
    "alembic_version",
}


def _table_exists(db_url: str, table_name: str) -> bool:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        result = table_name in inspect(conn).get_table_names()
    engine.dispose()
    return result


def _get_revision(db_url: str):
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        if "alembic_version" not in inspect(conn).get_table_names():
            return None
        rows = conn.execute(text("SELECT version_num FROM alembic_version")).fetchall()
    engine.dispose()
    return rows[0][0] if len(rows) == 1 else None


def _version_rows(db_url: str) -> int:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        if "alembic_version" not in inspect(conn).get_table_names():
            return 0
        count = conn.execute(text("SELECT COUNT(*) FROM alembic_version")).scalar()
    engine.dispose()
    return count


def _count_rows(db_url: str, table_name: str) -> int:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.connect() as conn:
        count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
    engine.dispose()
    return count


def _run_bootstrap() -> None:
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


@pytest.fixture
def pg_db(request):
    maintenance_url()
    db_name = unique_db_name(_TEST_DB_PREFIX, request.node.name)
    terminate_and_drop(db_name)
    create_db(db_name)
    os.environ["DATABASE_URL"] = per_test_db_url(db_name)

    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()
    yield db_name

    reset_engine()
    os.environ.pop("DATABASE_URL", None)
    get_settings.cache_clear()
    terminate_and_drop(db_name)


def _create_legacy_bookings_table(db_url: str) -> None:
    from sqlalchemy import Column, DateTime, Integer, String, func
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
        status = Column(String(32), nullable=False, server_default="requested")
        created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    Base.metadata.create_all(bind=engine, tables=[LegacyBooking.__table__])
    engine.dispose()


def _insert_legacy_bookings(db_url: str, count: int = 1) -> None:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    for i in range(1, count + 1):
        db.execute(
            text(
                "INSERT INTO bookings (service_type, visit_type, preferred_day, "
                "preferred_time, time_window, first_name, last_name, email, phone, "
                "reason_category) VALUES (:service_type, :visit_type, :preferred_day, "
                ":preferred_time, :time_window, :first_name, :last_name, :email, "
                ":phone, :reason_category)"
            ),
            {
                "service_type": "Urgent or acute care",
                "visit_type": "Clinic visit",
                "preferred_day": f"Monday {i}",
                "preferred_time": "9:00 AM",
                "time_window": "Morning",
                "first_name": f"Legacy{i}",
                "last_name": "Patient",
                "email": f"legacy{i}@example.com",
                "phone": f"+1-555-{i:04d}",
                "reason_category": "General appointment request",
            },
        )
    db.commit()
    db.close()
    engine.dispose()


def _create_empty_alembic_version(db_url: str) -> None:
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE alembic_version (version_num VARCHAR(32) PRIMARY KEY)"))
    engine.dispose()


def _stamp(db_url: str, revision: str) -> None:
    from alembic import command
    from alembic.config import Config
    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", db_url)
    command.stamp(cfg, revision)


def _upgrade(db_url: str, revision: str = "head") -> None:
    from alembic import command
    from alembic.config import Config
    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()
    cfg = Config("alembic.ini")
    cfg.set_main_option("sqlalchemy.url", db_url)
    command.upgrade(cfg, revision)


def test_fresh_database_reaches_current_head_and_is_idempotent(pg_db):
    _run_bootstrap()
    db_url = os.environ["DATABASE_URL"]

    for table in EXPECTED_TABLES:
        assert _table_exists(db_url, table), f"Table '{table}' is missing"
    assert _get_revision(db_url) == EXPECTED_HEAD

    _run_bootstrap()
    assert _get_revision(db_url) == EXPECTED_HEAD


def test_legacy_database_is_upgraded_without_losing_rows(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=3)

    _run_bootstrap()

    assert _get_revision(db_url) == EXPECTED_HEAD
    assert _count_rows(db_url, "bookings") == 3
    assert _table_exists(db_url, "appointment_attributions")


def test_empty_alembic_version_with_legacy_bookings_is_supported(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=1)
    _create_empty_alembic_version(db_url)

    assert _version_rows(db_url) == 0
    _run_bootstrap()

    assert _get_revision(db_url) == EXPECTED_HEAD
    assert _count_rows(db_url, "bookings") == 1


def test_incompatible_legacy_schema_fails_closed(pg_db):
    from app.migration_bootstrap import BootstrapError

    db_url = os.environ["DATABASE_URL"]
    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE bookings (id SERIAL PRIMARY KEY, service_type VARCHAR(128) NOT NULL)"
        ))
    engine.dispose()

    with pytest.raises(BootstrapError):
        _run_bootstrap()
    assert _get_revision(db_url) is None


def test_managed_0001_database_upgrades_to_current_head(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _insert_legacy_bookings(db_url, count=2)
    _stamp(db_url, "0001")

    _run_bootstrap()

    assert _get_revision(db_url) == EXPECTED_HEAD
    assert _count_rows(db_url, "bookings") == 2
    assert _table_exists(db_url, "appointment_attributions")


def test_current_head_database_passes_second_bootstrap(pg_db):
    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _stamp(db_url, "0001")
    _upgrade(db_url)
    assert _get_revision(db_url) == EXPECTED_HEAD

    _run_bootstrap()
    assert _get_revision(db_url) == EXPECTED_HEAD


def test_stamped_0001_with_0002_sentinel_fails_closed(pg_db):
    from app.migration_bootstrap import BootstrapError

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

    with pytest.raises(BootstrapError) as excinfo:
        _run_bootstrap()
    assert "inconsistent" in str(excinfo.value).lower()
    assert _get_revision(db_url) == "0001"
    assert _count_rows(db_url, "bookings") == 1


def test_stamped_0003_with_0004_sentinel_fails_closed(pg_db):
    """Protect the new attribution migration from partial prior application."""
    from app.migration_bootstrap import BootstrapError

    db_url = os.environ["DATABASE_URL"]
    _create_legacy_bookings_table(db_url)
    _stamp(db_url, "0001")
    _upgrade(db_url, "0003")
    assert _get_revision(db_url) == "0003"

    engine = create_engine(db_url, connect_args={"connect_timeout": 5})
    with engine.begin() as conn:
        conn.execute(text(
            "CREATE TABLE appointment_attributions ("
            "id SERIAL PRIMARY KEY, appointment_id INTEGER NOT NULL)"
        ))
    engine.dispose()

    with pytest.raises(BootstrapError) as excinfo:
        _run_bootstrap()
    message = str(excinfo.value).lower()
    assert "inconsistent" in message
    assert "appointment_attributions" in message
    assert _get_revision(db_url) == "0003"
