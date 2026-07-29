"""Tests for appointment confirmation email templates.

Uses SMTP_TEST_MODE=true — no real SMTP connection is ever made.
"""

import datetime
from unittest.mock import MagicMock, patch
from zoneinfo import ZoneInfo

import pytest

from app.core.config import get_settings
from app.core.database import reset_engine

CLINIC_TZ = ZoneInfo("America/Los_Angeles")

settings = get_settings()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
def test_app_setup():
    """Reload the FastAPI app for each test so module-level state is fresh."""
    import importlib
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_appt(first_name="Jane", last_name="Doe", email="jane@example.com",
               phone="+1-310-555-0189", reason="General appointment request",
               status="pending", appt_id=1, starts_at=None):
    """Build a mock Appointment with the minimum fields the templates need."""
    if starts_at is None:
        local = datetime.datetime(2026, 8, 4, 10, 0, tzinfo=CLINIC_TZ)
        starts_at = local.astimezone(datetime.timezone.utc)

    appt = MagicMock()
    appt.id = appt_id
    appt.first_name = first_name
    appt.last_name = last_name
    appt.email = email
    appt.phone = phone
    appt.reason_category = reason
    appt.status = status
    appt.starts_at = starts_at
    return appt


# ---------------------------------------------------------------------------
# Template builder unit tests
# ---------------------------------------------------------------------------

class TestPatientConfirmationTemplate:
    def test_subject_contains_dr_farah(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent or acute care")
        assert "Dr. Farah" in subject

    def test_body_contains_service_name(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "VIP or mobile visit")
        assert "VIP or mobile visit" in text
        assert "VIP or mobile visit" in html

    def test_body_contains_patient_name(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt(first_name="Maria", last_name="Garcia")
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "Maria" in text

    def test_body_contains_reference(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt(appt_id=42)
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "42" in text

    def test_body_contains_pacific_time(self):
        from app.emails.appointment import build_patient_confirmation
        local = datetime.datetime(2026, 8, 4, 10, 0, tzinfo=CLINIC_TZ)
        appt = _make_appt(starts_at=local.astimezone(datetime.timezone.utc))
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "August 04, 2026" in text
        assert "10:00 AM PT" in text

    def test_body_contains_emergency_line(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "911" in text

    def test_body_contains_clinic_phone(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "310-467-0101" in text

    def test_html_contains_table(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "<table" in html
        assert "</table>" in html

    def test_no_clinical_free_text(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        for forbidden in ("symptoms", "diagnosis", "medication"):
            assert forbidden not in text.lower()


class TestClinicNotificationTemplate:
    def test_subject_contains_patient_name(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(first_name="Carlos", last_name="Lopez")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "Carlos" in subject
        assert "Lopez" in subject

    def test_body_contains_patient_contact(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(email="carlos@test.com", phone="+1-555-000-1111")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "carlos@test.com" in text
        assert "+1-555-000-1111" in text

    def test_body_contains_reason_category(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(reason="General appointment request")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "General appointment request" in text

    def test_body_contains_reference(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(appt_id=7)
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "7" in text

    def test_body_contains_status(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(status="pending")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "pending" in text

    def test_html_contains_table(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt()
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "<table" in html


# ---------------------------------------------------------------------------
# Orchestrator unit tests
# ---------------------------------------------------------------------------

class TestSendAppointmentEmails:
    def test_calls_send_for_patient_and_clinic(self):
        from app.emails import appointment as mod
        appt = _make_appt(email="patient@test.com")

        with patch.object(mod, "_send_email_message") as mock_send:
            mock_send.return_value = True
            mod.send_appointment_emails(appt, "Urgent care")

            assert mock_send.call_count == 2
            # First call: patient confirmation
            patient_to = mock_send.call_args_list[0][0][0]
            assert patient_to == "patient@test.com"
            # Second call: clinic notification (sent to SMTP_FROM address)
            clinic_to = mock_send.call_args_list[1][0][0]
            assert "@" in clinic_to  # any valid email

    def test_patient_failure_does_not_block_clinic(self):
        from app.emails import appointment as mod
        appt = _make_appt()

        with patch.object(mod, "_send_email_message") as mock_send:
            # First call (patient) raises, second (clinic) succeeds.
            mock_send.side_effect = [RuntimeError("boom"), True]
            # Should not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 2

    def test_clinic_failure_does_not_block_patient(self):
        from app.emails import appointment as mod
        appt = _make_appt()

        with patch.object(mod, "_send_email_message") as mock_send:
            # First call (patient) succeeds, second (clinic) raises.
            mock_send.side_effect = [True, RuntimeError("boom")]
            # Should not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 2

    def test_never_raises_even_on_total_failure(self):
        from app.emails import appointment as mod
        appt = _make_appt()

        with patch.object(mod, "_send_email_message") as mock_send:
            mock_send.side_effect = RuntimeError("total failure")
            # Must not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 2


# ---------------------------------------------------------------------------
# Integration: email is triggered during appointment creation
# ---------------------------------------------------------------------------

class TestEmailTriggeredOnAppointmentCreate:
    def test_send_appointment_emails_called_on_201(self, seeded_db, test_app_setup):
        """Proof that the create handler invokes the email orchestrator."""
        from tests.test_appointments import (
            _next_working_day, _slot_at, VALID_APPOINTMENT,
        )
        from fastapi.testclient import TestClient

        app = test_app_setup
        y, m, d = _next_working_day(seeded_db)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }

        # Patch at the router's import site — it holds a module-level reference.
        with patch("app.routers.appointments.send_appointment_emails") as mock_send:
            with TestClient(app) as client:
                resp = client.post("/api/v1/appointments", json=payload)
                assert resp.status_code == 201, resp.text
                mock_send.assert_called_once()

                # Verify the call arguments.
                args, kwargs = mock_send.call_args
                called_appt = args[0]
                called_service_name = args[1]
                assert called_appt.id >= 1
                assert called_appt.email == "jane@example.com"
                assert called_service_name == "Urgent or acute care"

    def test_email_failure_still_returns_201(self, seeded_db, test_app_setup):
        """Best-effort: email failure must NOT affect the 201 response."""
        from tests.test_appointments import (
            _next_working_day, _slot_at, VALID_APPOINTMENT,
        )
        from fastapi.testclient import TestClient

        app = test_app_setup
        y, m, d = _next_working_day(seeded_db)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }

        with patch("app.routers.appointments.send_appointment_emails") as mock_send:
            mock_send.side_effect = RuntimeError("SMTP server on fire")
            with TestClient(app) as client:
                resp = client.post("/api/v1/appointments", json=payload)
                # Must still return 201 — the appointment is saved.
                assert resp.status_code == 201, resp.text
                body = resp.json()
                assert body["id"] >= 1
                assert body["status"] == "pending"

    def test_no_email_on_409(self, seeded_db, test_app_setup):
        """Email must NOT fire when the slot is already taken (409)."""
        from tests.test_appointments import (
            _next_working_day, _slot_at, VALID_APPOINTMENT,
        )
        from fastapi.testclient import TestClient

        app = test_app_setup
        y, m, d = _next_working_day(seeded_db)
        starts_at = _slot_at(y, m, d, 10, 0)
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": starts_at,
        }

        with patch("app.routers.appointments.send_appointment_emails") as mock_send:
            with TestClient(app) as client:
                # First creation — 201, email fires once.
                r1 = client.post("/api/v1/appointments", json=payload)
                assert r1.status_code == 201
                assert mock_send.call_count == 1

                # Second creation — 409, email must NOT fire again.
                r2 = client.post("/api/v1/appointments", json=payload)
                assert r2.status_code == 409
                assert mock_send.call_count == 1  # still 1, not 2
