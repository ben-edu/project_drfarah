"""Shared fixtures for scheduling tests.

Provides an isolated SQLite database per test with the full schema
(bookings + scheduling tables) created via create_all().
"""

import datetime
import os
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy.orm import Session


CLINIC_TZ = ZoneInfo("America/Los_Angeles")


def _make_utc(*, year, month, day, hour, minute):
    """Build a UTC-aware datetime from clinic-local wall-clock values."""
    local = datetime.datetime(year, month, day, hour, minute, tzinfo=CLINIC_TZ)
    return local.astimezone(datetime.timezone.utc)


@pytest.fixture(autouse=True)
def db_session(tmp_path):
    """Isolated SQLite database with all tables created.

    Each test gets a unique temporary database. No state leaks between tests.
    """
    from app.core.config import get_settings
    from app.core.database import Base, _get_engine, _SessionLocal, reset_engine

    # Import all models so they register with Base.metadata before create_all().
    import app.models.booking  # noqa: F401
    import app.models.service  # noqa: F401
    import app.models.working_hours  # noqa: F401
    import app.models.blocked_period  # noqa: F401
    import app.models.appointment  # noqa: F401
    import app.models.patient_registration  # noqa: F401

    saved = {}
    for k in (
        "DATABASE_URL", "ENVIRONMENT", "SMTP_HOST", "SMTP_TEST_MODE",
        "CLEANUP_TOKEN",
    ):
        saved[k] = os.environ.get(k)

    db_path = tmp_path / "test.db"
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SMTP_HOST"] = ""
    os.environ["SMTP_TEST_MODE"] = "true"
    os.environ["CLEANUP_TOKEN"] = "test-cleanup-token"

    get_settings.cache_clear()
    reset_engine()

    # Create all tables for the test.
    engine = _get_engine()
    Base.metadata.create_all(bind=engine)

    # Provide a session factory.
    from sqlalchemy.orm import sessionmaker
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        engine.dispose()
        reset_engine()
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        get_settings.cache_clear()


@pytest.fixture
def seed_services(db_session):
    """Insert provisional seed services matching the migration seed data."""
    from app.models.service import Service

    services = [
        Service(code="urgent-care", name="Urgent or acute care",
                description="Same-day illness or injury.",
                duration_minutes=30, buffer_before_minutes=0, buffer_after_minutes=0,
                is_active=True),
        Service(code="vip-mobile", name="VIP or mobile visit",
                description="Discreet hotel/office visits.",
                duration_minutes=45, buffer_before_minutes=15, buffer_after_minutes=15,
                is_active=True),
        Service(code="traveler-care", name="Traveler medical care",
                description="Care for visitors.",
                duration_minutes=30, buffer_before_minutes=0, buffer_after_minutes=0,
                is_active=True),
        Service(code="rejuvenation", name="Rejuvenation consultation",
                description="PRP, PRF consultations.",
                duration_minutes=60, buffer_before_minutes=15, buffer_after_minutes=15,
                is_active=True),
    ]
    db_session.add_all(services)
    db_session.commit()
    return services


@pytest.fixture
def seed_working_hours(db_session):
    """Insert provisional working hours: Mon-Fri 9am-5pm Pacific."""
    from app.models.working_hours import WorkingHours

    hours = []
    for d in range(0, 5):
        hours.append(WorkingHours(
            weekday=d,
            start_time=datetime.time(9, 0),
            end_time=datetime.time(17, 0),
            is_active=True,
            effective_from=datetime.date(2026, 1, 1),
        ))
    db_session.add_all(hours)
    db_session.commit()
    return hours


@pytest.fixture
def seeded_db(db_session, seed_services, seed_working_hours):
    """Database session with services and working hours already seeded."""
    return db_session


@pytest.fixture
def upcoming_monday():
    """Return the next Monday as a date string (YYYY-MM-DD)."""
    now = datetime.datetime.now(CLINIC_TZ)
    days_ahead = 0 - now.weekday()  # Monday = 0
    if days_ahead <= 0:
        days_ahead += 7
    monday = now.date() + datetime.timedelta(days=days_ahead)
    return monday.isoformat()
