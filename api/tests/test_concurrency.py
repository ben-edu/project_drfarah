"""Concurrency tests — double-booking protection under concurrent requests.

SQLite does NOT provide the same concurrency guarantees as PostgreSQL.
These tests verify the application-level conflict detection. The true
database-level protection is provided by the PostgreSQL exclusion
constraint in the migration.

For SQLite, we rely on SQLAlchemy's connection serialization within a
single process. These tests verify that the application-level conflict
check correctly rejects overlapping appointments.
"""

import datetime
import threading
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")


def _days_ahead(n):
    now = datetime.datetime.now(CLINIC_TZ)
    d = now.date() + datetime.timedelta(days=n)
    return d.year, d.month, d.day


def _slot_at(year, month, day, hour, minute):
    local = datetime.datetime(year, month, day, hour, minute, tzinfo=CLINIC_TZ)
    return local.astimezone(datetime.timezone.utc).isoformat()


@pytest.fixture(autouse=True)
def test_app_setup():
    import importlib
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


class TestConcurrency:
    def test_sequential_double_booking_returns_409(self, seeded_db, test_app_setup):
        """Application-level check: second insert for same slot gets 409."""
        app = test_app_setup
        y, m, d = _days_ahead(4)
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

    def test_concurrent_same_slot_one_wins(self, seeded_db, test_app_setup):
        """Two concurrent threads for the same slot — one succeeds, one gets 409.

        This test requires a database with true serializable isolation
        (PostgreSQL exclusion constraint). SQLite cannot prevent the
        race between SELECT-based conflict check and INSERT, so both
        threads may see an empty slot and both succeed.

        The sequential test above verifies that the application-level
        conflict detection works. This test documents the need for
        PostgreSQL's exclusion constraint in production.
        """
        import os

        db_url = os.environ.get("DATABASE_URL", "")
        if "sqlite" in db_url:
            pytest.skip(
                "SQLite cannot prevent the SELECT-then-INSERT race condition. "
                "PostgreSQL exclusion constraint provides this guarantee."
            )

        app = test_app_setup
        y, m, d = _days_ahead(4)
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

        def make_request():
            with TestClient(app) as client:
                resp = client.post("/api/v1/appointments", json=payload)
                results.append(resp.status_code)

        t1 = threading.Thread(target=make_request)
        t2 = threading.Thread(target=make_request)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

        # At least one must succeed, at least one must be 409.
        assert 201 in results, f"Expected at least one 201, got {results}"
        assert 409 in results, (
            f"Expected at least one 409 for double booking, got {results}"
        )
        assert len(results) == 2

    def test_overlapping_slot_rejected(self, seeded_db, test_app_setup):
        """A slot that starts during an existing appointment is rejected."""
        app = test_app_setup
        y, m, d = _days_ahead(4)

        # Book at 10:00 AM (30-min service).
        p1 = {
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
            "first_name": "A", "last_name": "B",
            "email": "a@b.com", "phone": "+1-555-000-0000",
            "reason_category": "Test",
        }
        # Try to book at 10:15 AM — overlaps the 10:00-10:30 appointment.
        p2 = {**p1, "starts_at": _slot_at(y, m, d, 10, 15),
              "first_name": "C"}

        with TestClient(app) as client:
            r1 = client.post("/api/v1/appointments", json=p1)
            assert r1.status_code == 201, r1.text
            r2 = client.post("/api/v1/appointments", json=p2)
            assert r2.status_code == 409, (
                f"Overlapping slot should be 409, got {r2.status_code}"
            )
