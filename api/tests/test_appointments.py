"""Tests for POST /api/v1/appointments — appointment creation."""

import datetime
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")


def _slot_at(year, month, day, hour, minute):
    """Return a UTC ISO timestamp for a clinic-local time."""
    local = datetime.datetime(year, month, day, hour, minute, tzinfo=CLINIC_TZ)
    return local.astimezone(datetime.timezone.utc).isoformat()


def _days_ahead(n):
    now = datetime.datetime.now(CLINIC_TZ)
    d = now.date() + datetime.timedelta(days=n)
    return d.year, d.month, d.day


@pytest.fixture(autouse=True)
def test_app_setup():
    import importlib
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


def _client(app):
    return TestClient(app)


VALID_APPOINTMENT = {
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "+1-310-555-0189",
    "reason_category": "General appointment request",
}


class TestAppointmentCreate:
    def test_creates_appointment_returns_201(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 201, resp.text

    def test_response_contains_required_fields(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            body = resp.json()
            assert body["id"] >= 1
            assert body["status"] == "pending"
            assert body["service_code"] == "urgent-care"
            assert body["first_name"] == "Jane"
            assert "ends_at" in body
            assert "created_at" in body

    def test_ends_at_derived_from_service_duration(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        starts_at = _slot_at(y, m, d, 10, 0)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": starts_at,
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            body = resp.json()
            starts = datetime.datetime.fromisoformat(body["starts_at"])
            ends = datetime.datetime.fromisoformat(body["ends_at"])
            diff = (ends - starts).total_seconds() / 60
            assert diff == 30  # urgent-care is 30 min

    def test_409_on_double_booking(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        starts_at = _slot_at(y, m, d, 10, 0)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": starts_at,
        }
        with _client(app) as client:
            r1 = client.post("/api/v1/appointments", json=payload)
            assert r1.status_code == 201
            r2 = client.post("/api/v1/appointments", json=payload)
            assert r2.status_code == 409, r2.text

    def test_422_for_past_slot(self, seeded_db, test_app_setup):
        app = test_app_setup
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(2020, 1, 1, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 422

    def test_422_outside_working_hours(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 7, 0),  # 7 AM, before 9 AM open
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 422

    def test_404_for_unknown_service(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "nonexistent",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 404

    def test_409_blocked_period(self, seeded_db, test_app_setup):
        app = test_app_setup
        from app.models.blocked_period import BlockedPeriod
        from app.models.working_hours import WorkingHours
        from app.models.service import Service

        # Query an active working-hour record from the seeded database.
        wh = seeded_db.query(WorkingHours).filter(
            WorkingHours.is_active == True
        ).first()
        assert wh is not None, "No active working hours in seed data"

        # Get the urgent-care service for its duration.
        svc = seeded_db.query(Service).filter(
            Service.code == "urgent-care"
        ).first()
        assert svc is not None

        # Find the next future occurrence of this working-hour weekday.
        today = datetime.datetime.now(CLINIC_TZ).date()
        days_until = (wh.weekday - today.weekday()) % 7
        if days_until == 0:
            days_until = 7  # Use next week to avoid edge cases with today
        target_date = today + datetime.timedelta(days=days_until)

        # Choose a slot one hour after opening.
        slot_hour = wh.start_time.hour + 1
        slot_minute = wh.start_time.minute

        # Ensure the service duration fits before the working interval ends.
        slot_end_minutes = slot_hour * 60 + slot_minute + svc.duration_minutes
        interval_end_minutes = wh.end_time.hour * 60 + wh.end_time.minute
        assert slot_end_minutes <= interval_end_minutes, (
            "Service duration exceeds working hours interval"
        )

        local_start = datetime.datetime(
            target_date.year, target_date.month, target_date.day,
            slot_hour, slot_minute, tzinfo=CLINIC_TZ,
        )
        utc_start = local_start.astimezone(datetime.timezone.utc)

        # Blocked period covers one hour from the slot start.
        local_end = local_start + datetime.timedelta(hours=1)
        utc_end = local_end.astimezone(datetime.timezone.utc)

        bp = BlockedPeriod(
            starts_at=utc_start,
            ends_at=utc_end,
            reason="Test blocked period",
            is_active=True,
        )
        seeded_db.add(bp)
        seeded_db.commit()

        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": utc_start.isoformat(),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 409, resp.text
            body = resp.json()
            assert "blocked" in body.get("detail", "").lower()

    def test_cancelled_appointment_does_not_block(self, seeded_db, test_app_setup):
        """A cancelled appointment should not block the same slot."""
        from app.models.appointment import Appointment
        from app.models.service import Service
        app = test_app_setup
        y, m, d = _days_ahead(4)
        svc = seeded_db.query(Service).filter(Service.code == "urgent-care").first()

        starts_utc = datetime.datetime.fromisoformat(_slot_at(y, m, d, 10, 0))
        duration = datetime.timedelta(minutes=svc.duration_minutes)
        cancelled = Appointment(
            service_id=svc.id,
            starts_at=starts_utc,
            ends_at=starts_utc + duration,
            first_name="X", last_name="Y", email="x@x.com", phone="0",
            reason_category="Test", status="cancelled",
        )
        seeded_db.add(cancelled)
        seeded_db.commit()

        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 201, resp.text

    def test_no_sensitive_fields_in_response(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            text = resp.text.lower()
            for forbidden in ("password", "token", "secret", "smtp",
                              "psycopg", "database_url", "stack", "traceback"):
                assert forbidden not in text, f"'{forbidden}' found in response"

    def test_422_invalid_email(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
            "email": "not-an-email",
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 422

    def test_422_no_timezone_offset(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": f"{y}-{m:02d}-{d:02d}T10:00:00",  # naive
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 422

    def test_422_empty_first_name(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
            "first_name": "",
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 422

    def test_source_defaults_to_none(self, seeded_db, test_app_setup):
        app = test_app_setup
        y, m, d = _days_ahead(4)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            body = resp.json()
            assert body.get("source") is None or "source" not in body

    def test_cleanup_ci_requires_token(self, seeded_db, test_app_setup):
        """Cleanup endpoint rejects requests without a valid token."""
        app = test_app_setup
        with _client(app) as client:
            resp = client.post("/api/v1/internal/cleanup-ci")
            assert resp.status_code == 401

    def test_cleanup_ci_with_valid_token(self, seeded_db, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.post(
                "/api/v1/internal/cleanup-ci",
                headers={"Authorization": "Bearer test-cleanup-token"},
            )
            assert resp.status_code == 200
            body = resp.json()
            assert "deleted" in body

    def test_vip_mobile_buffer_respected(self, seeded_db, test_app_setup):
        """VIP mobile visit has 15-min buffer before and after."""
        app = test_app_setup
        y, m, d = _days_ahead(4)
        # Book at 9:15 AM — the 15-min buffer before pushes occupied start to 9:00 AM,
        # which is exactly at opening time (valid).
        starts_at = _slot_at(y, m, d, 9, 15)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "vip-mobile",
            "starts_at": starts_at,
        }
        with _client(app) as client:
            resp = client.post("/api/v1/appointments", json=payload)
            assert resp.status_code == 201
            body = resp.json()
            starts = datetime.datetime.fromisoformat(body["starts_at"])
            ends = datetime.datetime.fromisoformat(body["ends_at"])
            diff = (ends - starts).total_seconds() / 60
            assert diff == 45  # vip-mobile is 45 min service
