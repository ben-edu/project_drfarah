"""Tests for first-party acquisition attribution on scheduled appointments."""

import datetime
from unittest.mock import patch
from zoneinfo import ZoneInfo

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")


@pytest.fixture(autouse=True)
def test_app_setup():
    import importlib
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


def _client(app):
    return TestClient(app)


def _next_working_day(db):
    from app.models.working_hours import WorkingHours

    wh = db.query(WorkingHours).filter(WorkingHours.is_active == True).first()
    assert wh is not None
    today = datetime.datetime.now(CLINIC_TZ).date()
    days_until = (wh.weekday - today.weekday()) % 7
    if days_until == 0:
        days_until = 7
    return today + datetime.timedelta(days=days_until)


def _slot_at(day, hour=10, minute=0):
    local = datetime.datetime(
        day.year, day.month, day.day, hour, minute, tzinfo=CLINIC_TZ
    )
    return local.astimezone(datetime.timezone.utc).isoformat()


def _payload(db):
    day = _next_working_day(db)
    return {
        "service_code": "urgent-care",
        "starts_at": _slot_at(day),
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "+1-310-555-0189",
        "reason_category": "General appointment request",
    }


class TestAppointmentAttribution:
    def test_structured_attribution_is_saved_and_sets_legacy_source(
        self, seeded_db, test_app_setup
    ):
        from app.models.appointment import Appointment
        from app.models.appointment_attribution import AppointmentAttribution
        from app.routers import appointments as router

        payload = _payload(seeded_db)
        payload["source"] = "web"
        payload["attribution"] = {
            "marketing_session_id": "mkt-test-123",
            "first_touch": {
                "source": "google_ads",
                "utm_source": "google",
                "utm_medium": "cpc",
                "utm_campaign": "urgent-care-beverly-hills",
                "gclid": "TestGclidABC123",
                "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            },
            "last_touch": {
                "source": "google_ads",
                "utm_source": "google",
                "utm_medium": "cpc",
                "utm_campaign": "urgent-care-beverly-hills",
                "gclid": "TestGclidABC123",
                "captured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            },
            "partner_code": None,
            "traveler_segment": "unknown",
            "attribution_version": "v1",
        }

        with patch.object(router, "send_appointment_emails"):
            with _client(test_app_setup) as client:
                response = client.post("/api/v1/appointments", json=payload)

        assert response.status_code == 201, response.text
        appointment_id = response.json()["id"]

        seeded_db.expire_all()
        appointment = seeded_db.query(Appointment).filter(Appointment.id == appointment_id).one()
        attribution = (
            seeded_db.query(AppointmentAttribution)
            .filter(AppointmentAttribution.appointment_id == appointment_id)
            .one()
        )

        assert appointment.source == "google_ads"
        assert attribution.marketing_session_id == "mkt-test-123"
        assert attribution.first_touch["source"] == "google_ads"
        assert attribution.last_touch["gclid"] == "TestGclidABC123"
        assert attribution.traveler_segment == "unknown"
        assert "reason_category" not in attribution.last_touch
        assert "email" not in attribution.last_touch

    def test_partner_and_traveler_markers_are_saved_without_clinical_data(
        self, seeded_db, test_app_setup
    ):
        from app.models.appointment_attribution import AppointmentAttribution
        from app.routers import appointments as router

        payload = _payload(seeded_db)
        payload["attribution"] = {
            "marketing_session_id": "mkt-partner-1",
            "first_touch": {"source": "hotel_concierge"},
            "last_touch": {"source": "hotel_concierge"},
            "partner_code": "hotel-beverly-001",
            "traveler_segment": "yes",
            "attribution_version": "v1",
        }

        with patch.object(router, "send_appointment_emails"):
            with _client(test_app_setup) as client:
                response = client.post("/api/v1/appointments", json=payload)

        assert response.status_code == 201, response.text
        appointment_id = response.json()["id"]
        seeded_db.expire_all()
        attribution = (
            seeded_db.query(AppointmentAttribution)
            .filter(AppointmentAttribution.appointment_id == appointment_id)
            .one()
        )
        assert attribution.partner_code == "hotel-beverly-001"
        assert attribution.traveler_segment == "yes"

    def test_invalid_traveler_segment_is_rejected(self, seeded_db, test_app_setup):
        payload = _payload(seeded_db)
        payload["attribution"] = {
            "marketing_session_id": "mkt-invalid-1",
            "first_touch": {"source": "direct"},
            "last_touch": {"source": "direct"},
            "traveler_segment": "maybe",
        }

        with _client(test_app_setup) as client:
            response = client.post("/api/v1/appointments", json=payload)
        assert response.status_code == 422

    def test_nested_ci_source_cannot_bypass_reserved_source_guard(
        self, seeded_db, test_app_setup
    ):
        payload = _payload(seeded_db)
        payload["source"] = "web"
        payload["attribution"] = {
            "marketing_session_id": "mkt-ci-bypass",
            "first_touch": {"source": "ci"},
            "last_touch": {"source": "ci"},
            "traveler_segment": "unknown",
        }

        with _client(test_app_setup) as client:
            response = client.post("/api/v1/appointments", json=payload)
        assert response.status_code == 403

    def test_authorized_ci_marker_stays_ci_even_with_nested_attribution(
        self, seeded_db, test_app_setup, monkeypatch
    ):
        """Smoke-test cleanup/email semantics must win over marketing metadata."""
        from app.models.appointment import Appointment
        from app.routers import appointments as router

        monkeypatch.setattr(router.settings, "ENVIRONMENT", "staging")
        monkeypatch.setattr(router.settings, "CLEANUP_TOKEN", "test-ci-secret")

        payload = _payload(seeded_db)
        payload["source"] = "ci"
        payload["attribution"] = {
            "marketing_session_id": "mkt-ci-authorized",
            "first_touch": {"source": "google_ads", "gclid": "SmokeTestClickId"},
            "last_touch": {"source": "google_ads", "gclid": "SmokeTestClickId"},
            "traveler_segment": "unknown",
        }

        with patch.object(router, "send_appointment_emails") as send:
            with _client(test_app_setup) as client:
                response = client.post(
                    "/api/v1/appointments",
                    json=payload,
                    headers={"X-CI-Token": "test-ci-secret"},
                )

        assert response.status_code == 201, response.text
        seeded_db.expire_all()
        appointment = (
            seeded_db.query(Appointment)
            .filter(Appointment.id == response.json()["id"])
            .one()
        )
        assert appointment.source == "ci"
        send.assert_not_called()
