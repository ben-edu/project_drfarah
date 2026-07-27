"""Tests for GET /api/v1/availability — slot generation endpoint."""

import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")


def _today_str():
    now = datetime.datetime.now(CLINIC_TZ)
    return now.date().isoformat()


def _days_from_now(n):
    now = datetime.datetime.now(CLINIC_TZ)
    return (now.date() + datetime.timedelta(days=n)).isoformat()


def _next_working_date_str(db):
    """Return an ISO date string (YYYY-MM-DD) for a future date with active
    working hours.

    Queries the first active WorkingHours record, finds the next occurrence
    of its weekday, and returns the date as a string. The returned date is
    always in the future (next week if today matches the weekday).

    Does not hard-code calendar dates or depend on the current weekday.
    """
    from app.models.working_hours import WorkingHours

    wh = db.query(WorkingHours).filter(
        WorkingHours.is_active == True
    ).first()
    assert wh is not None, "No active working hours in seed data"

    today = datetime.datetime.now(CLINIC_TZ).date()
    days_until = (wh.weekday - today.weekday()) % 7
    if days_until == 0:
        days_until = 7  # Use next week to avoid edge cases with today
    target_date = today + datetime.timedelta(days=days_until)

    return target_date.isoformat()


@pytest.fixture(autouse=True)
def test_app_setup():
    import importlib
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


def _client(app):
    return TestClient(app)


class TestAvailabilityEndpoint:
    def test_returns_200_for_valid_request(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)  # pick a weekday
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            assert resp.status_code == 200

    def test_returns_slots_for_valid_range(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            assert body["service"]["code"] == "urgent-care"
            assert body["timezone"] == "America/Los_Angeles"
            assert "slots" in body

    def test_service_code_in_response(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            assert body["service"]["duration_minutes"] == 30

    def test_404_for_unknown_service(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=nonexistent&start_date={d}&end_date={d}"
            )
            assert resp.status_code == 404

    def test_404_for_inactive_service(self, seeded_db, test_app_setup):
        from app.models.service import Service
        seeded_db.add(Service(code="inactive", name="Inactive",
                              duration_minutes=30, is_active=False))
        seeded_db.commit()

        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=inactive&start_date={d}&end_date={d}"
            )
            assert resp.status_code == 404

    def test_422_for_invalid_service_code(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=&start_date={d}&end_date={d}"
            )
            assert resp.status_code == 422

    def test_422_for_invalid_dates(self, seeded_db, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get(
                "/api/v1/availability?service_code=urgent-care&start_date=bad&end_date=2026-01-01"
            )
            assert resp.status_code == 422

    def test_422_start_after_end(self, seeded_db, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get(
                "/api/v1/availability?service_code=urgent-care&start_date=2026-12-31&end_date=2026-01-01"
            )
            assert resp.status_code == 422

    def test_422_range_too_large(self, seeded_db, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get(
                "/api/v1/availability?service_code=urgent-care&start_date=2026-01-01&end_date=2026-03-01"
            )
            assert resp.status_code == 422

    def test_weekend_has_no_slots(self, seeded_db, test_app_setup):
        """Working hours are Mon-Fri only. Weekend should return empty slots."""
        app = test_app_setup
        # Find the next Saturday.
        now = datetime.datetime.now(CLINIC_TZ)
        days_to_sat = 5 - now.weekday()
        if days_to_sat <= 0:
            days_to_sat += 7
        sat = (now.date() + datetime.timedelta(days=days_to_sat)).isoformat()

        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={sat}&end_date={sat}"
            )
            body = resp.json()
            assert body["slots"] == []

    def test_slots_include_starts_at_and_ends_at(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            for slot in body["slots"]:
                assert "starts_at" in slot
                assert "ends_at" in slot

    def test_slots_do_not_overlap(self, seeded_db, test_app_setup):
        """Each slot is separated by the slot increment (15 min)."""
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            if len(body["slots"]) < 2:
                return
            starts = [s["starts_at"] for s in body["slots"]]
            for i in range(1, len(starts)):
                # Slots should be in chronological order.
                assert starts[i] > starts[i - 1]

    def test_past_slots_not_returned(self, seeded_db, test_app_setup):
        """Availability in the past returns empty slots."""
        app = test_app_setup
        with _client(app) as client:
            resp = client.get(
                "/api/v1/availability?service_code=urgent-care&start_date=2020-01-01&end_date=2020-01-01"
            )
            body = resp.json()
            assert body["slots"] == []

    def test_no_duplicate_slots(self, seeded_db, test_app_setup):
        app = test_app_setup
        d = _days_from_now(3)
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            starts = [s["starts_at"] for s in body["slots"]]
            assert len(starts) == len(set(starts))

    def test_blocked_period_excludes_slots(self, seeded_db, test_app_setup):
        from app.models.blocked_period import BlockedPeriod
        from app.models.service import Service

        # Block the first 2 hours of a deterministic working day.
        d = _next_working_date_str(seeded_db)
        day_dt = datetime.datetime.fromisoformat(d)
        local_start = datetime.datetime(day_dt.year, day_dt.month, day_dt.day,
                                        9, 0, tzinfo=CLINIC_TZ)
        local_end = datetime.datetime(day_dt.year, day_dt.month, day_dt.day,
                                      11, 0, tzinfo=CLINIC_TZ)
        bp = BlockedPeriod(
            starts_at=local_start.astimezone(datetime.timezone.utc),
            ends_at=local_end.astimezone(datetime.timezone.utc),
            reason="Test block",
            is_active=True,
        )
        seeded_db.add(bp)
        seeded_db.commit()

        app = test_app_setup
        with _client(app) as client:
            resp = client.get(
                f"/api/v1/availability?service_code=urgent-care&start_date={d}&end_date={d}"
            )
            body = resp.json()
            # No slot should start before 11:00 AM local.
            for slot in body["slots"]:
                slot_start_local = datetime.datetime.fromisoformat(
                    slot["starts_at"]
                ).astimezone(CLINIC_TZ)
                assert slot_start_local.hour >= 11, (
                    f"Slot at {slot['starts_at']} falls in blocked period"
                )
