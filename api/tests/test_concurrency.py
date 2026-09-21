"""Concurrency tests — double-booking protection.

Two layers are exercised:

1. Application-level conflict detection (SQLite, in the default test stage):
   the SELECT-then-check in the router rejects a second overlapping
   appointment with HTTP 409. Deterministic dates are used (next Monday)
   so a slot always lands inside seeded working hours.

2. Database-level protection (PostgreSQL, marked @pytest.mark.postgresql):
   the real exclusion constraint created by migration 0002 guarantees that
   two genuinely concurrent requests for the same slot yield exactly one
   201 and one 409. This runs in the dedicated PostgreSQL CI stage.
"""

import datetime
import importlib
import os
import threading
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")

_PG_PREFIX = "drfarah_concurrency_test_"


def _next_monday():
    """Return (year, month, day) for the next Monday (never today).

    Always a seeded working day (Mon-Fri 9-17) and always in the future.
    """
    now = datetime.datetime.now(CLINIC_TZ)
    days_ahead = (0 - now.weekday()) % 7  # Monday == 0
    if days_ahead == 0:
        days_ahead = 7
    d = now.date() + datetime.timedelta(days=days_ahead)
    return d.year, d.month, d.day


def _slot_at(year, month, day, hour, minute):
    local = datetime.datetime(year, month, day, hour, minute, tzinfo=CLINIC_TZ)
    return local.astimezone(datetime.timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# Application-level checks (SQLite stage).
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def test_app_setup():
    """Reload the app so it binds to the fixture-provided (SQLite) database."""
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


class TestConcurrency:
    def test_sequential_double_booking_returns_409(self, seeded_db, test_app_setup):
        """Application-level check: a second insert for the same slot gets 409."""
        app = test_app_setup
        y, m, d = _next_monday()
        starts_at = _slot_at(y, m, d, 10, 0)
        payload = {
            "service_code": "urgent-care",
            "starts_at": starts_at,
            "first_name": "Test",
            "last_name": "User",
            "email": "test@example.com",
            "phone": "+1-555-000-0000",
            "reason_category": "Test",
        }
        with TestClient(app) as client:
            r1 = client.post("/api/v1/appointments", json=payload)
            assert r1.status_code == 201, r1.text
            r2 = client.post("/api/v1/appointments", json=payload)
            assert r2.status_code == 409, (
                f"Expected 409 for double booking, got {r2.status_code}: {r2.text}"
            )

    def test_overlapping_slot_rejected(self, seeded_db, test_app_setup):
        """A slot that starts during an existing appointment is rejected."""
        app = test_app_setup
        y, m, d = _next_monday()

        # Book at 10:00 (30-min service).
        p1 = {
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
            "first_name": "A", "last_name": "B",
            "email": "a@b.com", "phone": "+1-555-000-0000",
            "reason_category": "Test",
        }
        # Try to book at 10:15 — overlaps the 10:00-10:30 appointment.
        p2 = {**p1, "starts_at": _slot_at(y, m, d, 10, 15), "first_name": "C"}

        with TestClient(app) as client:
            r1 = client.post("/api/v1/appointments", json=p1)
            assert r1.status_code == 201, r1.text
            r2 = client.post("/api/v1/appointments", json=p2)
            assert r2.status_code == 409, (
                f"Overlapping slot should be 409, got {r2.status_code}"
            )


# ---------------------------------------------------------------------------
# Database-level protection (PostgreSQL stage).
# ---------------------------------------------------------------------------


@pytest.fixture
def pg_scheduling_app(request):
    """Disposable PostgreSQL database, fully migrated + seeded, bound to the app.

    Migration 0002 creates the `no_double_booking` exclusion constraint and
    seeds services + working hours. The app is reloaded so it uses the
    PostgreSQL engine. Cleanup drops the database even on failure.
    """
    from tests._pg_util import (
        create_db,
        maintenance_url,
        per_test_db_url,
        terminate_and_drop,
        unique_db_name,
    )

    maintenance_url()  # clean skip if no server is provided.

    db_name = unique_db_name(_PG_PREFIX, request.node.name)
    terminate_and_drop(db_name)
    create_db(db_name)

    os.environ["DATABASE_URL"] = per_test_db_url(db_name)
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SMTP_TEST_MODE"] = "true"
    os.environ["CLEANUP_TOKEN"] = "test-token"

    from app.core.config import get_settings
    from app.core.database import reset_engine as _reset

    get_settings.cache_clear()
    _reset()

    # Real migration path: creates tables, the exclusion constraint, and seeds.
    from app.migration_bootstrap import main as bootstrap_main
    bootstrap_main()

    # Reload the app so it binds to the (now warm) PostgreSQL engine.
    import app.main
    importlib.reload(app.main)

    yield app.main.app

    _reset()
    os.environ.pop("DATABASE_URL", None)
    get_settings.cache_clear()
    terminate_and_drop(db_name)


@pytest.mark.postgresql
class TestConcurrencyPostgres:
    """True concurrency guaranteed by the PostgreSQL exclusion constraint."""

    def test_concurrent_same_slot_one_wins(self, pg_scheduling_app):
        """Two concurrent requests for the same slot: one 201, one 409."""
        app = pg_scheduling_app
        y, m, d = _next_monday()
        starts_at = _slot_at(y, m, d, 10, 0)
        payload = {
            "service_code": "urgent-care",
            "starts_at": starts_at,
            "first_name": "Concurrent",
            "last_name": "Test",
            "email": "concurrent@example.com",
            "phone": "+1-555-999-0000",
            "reason_category": "Test",
        }

        results = []
        errors = []

        def make_request():
            try:
                with TestClient(app) as client:
                    resp = client.post("/api/v1/appointments", json=payload)
                    results.append(resp.status_code)
            except Exception as exc:  # pragma: no cover - surfaced via assert
                errors.append(repr(exc))

        t1 = threading.Thread(target=make_request)
        t2 = threading.Thread(target=make_request)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        assert not errors, f"Unexpected exceptions: {errors}"
        assert sorted(results) == [201, 409], (
            f"Expected exactly one 201 and one 409, got {results}"
        )

        # Exactly one active appointment row must exist for the slot.
        from sqlalchemy import text
        from app.core.database import _get_engine

        engine = _get_engine()
        with engine.connect() as conn:
            active = conn.execute(
                text(
                    "SELECT COUNT(*) FROM appointments "
                    "WHERE status NOT IN ('cancelled', 'no_show')"
                )
            ).scalar()
        assert active == 1, f"Expected 1 active appointment, found {active}"
