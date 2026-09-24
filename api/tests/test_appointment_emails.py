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

    def test_body_excludes_service_name(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "VIP or mobile visit")
        assert "VIP or mobile visit" not in text
        assert "VIP or mobile visit" not in html

    def test_body_excludes_patient_name(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt(first_name="Maria", last_name="Garcia")
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "Maria" not in text
        assert "Garcia" not in text
        assert "Maria" not in html
        assert "Garcia" not in html

    def test_body_excludes_reference(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt(appt_id=42)
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "42" not in text
        assert "42" not in html

    def test_body_excludes_appointment_time(self):
        from app.emails.appointment import build_patient_confirmation
        local = datetime.datetime(2026, 8, 4, 10, 0, tzinfo=CLINIC_TZ)
        appt = _make_appt(starts_at=local.astimezone(datetime.timezone.utc))
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "August 04, 2026" not in text
        assert "10:00 AM PT" not in text
        assert "August 04, 2026" not in html
        assert "10:00 AM PT" not in html

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

    def test_html_contains_privacy_notice(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        assert "appointment details are not included" in html
        assert "<table" not in html

    def test_no_clinical_free_text(self):
        from app.emails.appointment import build_patient_confirmation
        appt = _make_appt()
        subject, text, html = build_patient_confirmation(appt, "Urgent care")
        for forbidden in ("symptoms", "diagnosis", "medication"):
            assert forbidden not in text.lower()


class TestClinicNotificationTemplate:
    def test_subject_excludes_patient_name(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(first_name="Carlos", last_name="Lopez")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "Carlos" not in subject
        assert "Lopez" not in subject

    def test_body_excludes_patient_contact(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(email="carlos@test.com", phone="+1-555-000-1111")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "carlos@test.com" not in text
        assert "+1-555-000-1111" not in text
        assert "carlos@test.com" not in html
        assert "+1-555-000-1111" not in html

    def test_body_excludes_reason_category(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(reason="General appointment request")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "General appointment request" not in text
        assert "General appointment request" not in html

    def test_body_excludes_reference(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(appt_id=987654321)
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "987654321" not in text
        assert "987654321" not in html

    def test_body_excludes_status(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt(status="pending")
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert "pending" not in text
        assert "pending" not in html

    def test_body_links_to_secure_admin_portal(self):
        from app.emails.appointment import build_clinic_notification
        appt = _make_appt()
        subject, text, html = build_clinic_notification(appt, "Urgent care")
        assert settings.ADMIN_PORTAL_URL in text
        assert settings.ADMIN_PORTAL_URL in html
        assert "<table" not in html


# ---------------------------------------------------------------------------
# Orchestrator unit tests
# ---------------------------------------------------------------------------

class TestSendAppointmentEmails:
    def test_calls_send_for_patient_and_each_clinic_recipient(self, monkeypatch):
        from app.emails import appointment as mod
        appt = _make_appt(email="patient@test.com")
        monkeypatch.setattr(
            mod.settings,
            "SMTP_TO",
            "clinic-primary@example.com,clinic-secondary@example.com",
        )

        with patch.object(mod, "_send_email_message") as mock_send:
            mock_send.return_value = True
            mod.send_appointment_emails(appt, "Urgent care")

            assert mock_send.call_count == 3
            # First call: patient confirmation (4 args: to, subj, text, html)
            patient_args = mock_send.call_args_list[0][0]
            assert patient_args[0] == "patient@test.com"
            assert len(patient_args) == 4  # text + html both passed
            clinic_recipients = [
                call.args[0] for call in mock_send.call_args_list[1:]
            ]
            assert clinic_recipients == [
                "clinic-primary@example.com",
                "clinic-secondary@example.com",
            ]
            assert all(len(call.args) == 4 for call in mock_send.call_args_list[1:])

    def test_patient_failure_does_not_block_clinic(self, monkeypatch):
        from app.emails import appointment as mod
        appt = _make_appt()
        monkeypatch.setattr(
            mod.settings,
            "SMTP_TO",
            "clinic-primary@example.com,clinic-secondary@example.com",
        )

        with patch.object(mod, "_send_email_message") as mock_send:
            # Patient raises; both clinic deliveries still run.
            mock_send.side_effect = [RuntimeError("boom"), True, True]
            # Should not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 3

    def test_one_clinic_failure_does_not_block_other_recipient(self, monkeypatch):
        from app.emails import appointment as mod
        appt = _make_appt()
        monkeypatch.setattr(
            mod.settings,
            "SMTP_TO",
            "clinic-primary@example.com,clinic-secondary@example.com",
        )

        with patch.object(mod, "_send_email_message") as mock_send:
            # Patient succeeds; first clinic fails; second clinic still runs.
            mock_send.side_effect = [True, RuntimeError("boom"), True]
            # Should not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 3

    def test_never_raises_even_on_total_failure(self, monkeypatch):
        from app.emails import appointment as mod
        appt = _make_appt()
        monkeypatch.setattr(
            mod.settings,
            "SMTP_TO",
            "clinic-primary@example.com,clinic-secondary@example.com",
        )

        with patch.object(mod, "_send_email_message") as mock_send:
            mock_send.side_effect = RuntimeError("total failure")
            # Must not raise.
            mod.send_appointment_emails(appt, "Urgent care")
            assert mock_send.call_count == 3


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

    def test_no_email_for_ci_source(self, seeded_db, test_app_setup):
        """source="ci" appointments must NOT trigger email."""
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
            "source": "ci",
        }

        with patch("app.routers.appointments.send_appointment_emails") as mock_send:
            with TestClient(app) as client:
                resp = client.post("/api/v1/appointments", json=payload)
                assert resp.status_code == 201, resp.text
                mock_send.assert_not_called()

    def test_email_still_fires_for_normal_source(self, seeded_db, test_app_setup):
        """Non-CI appointments (source omitted or "web") must trigger email."""
        from tests.test_appointments import (
            _next_working_day, _slot_at, VALID_APPOINTMENT,
        )
        from fastapi.testclient import TestClient

        app = test_app_setup
        y, m, d = _next_working_day(seeded_db)
        # No source field — defaults to None, treated as normal booking.
        payload = {
            **VALID_APPOINTMENT,
            "service_code": "urgent-care",
            "starts_at": _slot_at(y, m, d, 10, 0),
        }

        with patch("app.routers.appointments.send_appointment_emails") as mock_send:
            with TestClient(app) as client:
                resp = client.post("/api/v1/appointments", json=payload)
                assert resp.status_code == 201, resp.text
                mock_send.assert_called_once()


# ---------------------------------------------------------------------------
# Unit tests: _send_email_message multipart/alternative behaviour
# ---------------------------------------------------------------------------

@pytest.fixture
def _smtp_env_for_multipart():
    """Temporarily set SMTP env so _send_email_message runs the real path."""
    import os
    saved = {}
    for k in (
        "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
        "SMTP_FROM", "SMTP_TO", "SMTP_USE_TLS", "SMTP_TEST_MODE",
        "ADMIN_PORTAL_URL",
    ):
        saved[k] = os.environ.get(k)
    os.environ["SMTP_HOST"] = "smtp-relay.brevo.com"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USER"] = "test-login@smtp-brevo.com"
    os.environ["SMTP_PASSWORD"] = "test-password"
    os.environ["SMTP_FROM"] = "notifications@drfarahvipurgentcare.com"
    os.environ["SMTP_TO"] = (
        "clinic-primary@example.com,clinic-secondary@example.com"
    )
    os.environ["SMTP_USE_TLS"] = "true"
    os.environ["SMTP_TEST_MODE"] = "false"
    os.environ["ADMIN_PORTAL_URL"] = "https://admin-staging.drfarahvipurgentcare.com"

    from app.core.config import get_settings
    get_settings.cache_clear()

    import importlib
    import app.services.email
    importlib.reload(app.services.email)

    yield

    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    get_settings.cache_clear()
    importlib.reload(app.services.email)


class TestSendEmailMessageMultipart:
    def test_multipart_alternative_when_html_given(self, _smtp_env_for_multipart):
        """When html_body is provided the message must be multipart/alternative."""
        from unittest.mock import MagicMock, patch
        from app.services.email import _send_email_message

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            _send_email_message(
                "to@example.com",
                "Test subject",
                "Plain text body",
                "<p>HTML body</p>",
            )

            sent_msg = mock_server.send_message.call_args[0][0]
            # Must be multipart/alternative with two sub-parts.
            assert sent_msg.get_content_type() == "multipart/alternative"
            parts = list(sent_msg.walk())
            # parts[0] is the top-level multipart/alternative; parts[1:] are leaves.
            subtypes = {p.get_content_type() for p in parts[1:]}
            assert "text/plain" in subtypes
            assert "text/html" in subtypes

    def test_plain_only_when_no_html(self, _smtp_env_for_multipart):
        """When html_body is None the message stays text/plain."""
        from unittest.mock import MagicMock, patch
        from app.services.email import _send_email_message

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            _send_email_message(
                "to@example.com",
                "Test subject",
                "Plain text only",
            )

            sent_msg = mock_server.send_message.call_args[0][0]
            assert sent_msg.get_content_type() == "text/plain"
            assert sent_msg.get_content() == "Plain text only\n"

    def test_legacy_caller_still_works(self, _smtp_env_for_multipart):
        """send_booking_notification (3-arg call) still sends plain-text only."""
        from unittest.mock import MagicMock, patch
        from app.services.email import send_booking_notification

        booking = {
            "first_name": "Jane",
            "last_name": "Doe",
            "service_type": "Urgent or acute care",
            "visit_type": "Clinic visit",
            "preferred_day": "Monday, July 27",
            "preferred_time": "10:00 AM",
            "time_window": "Late morning",
            "reason_category": "General appointment request",
            "email": "jane@example.com",
            "phone": "+1-310-555-0189",
        }

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = send_booking_notification(booking)
            assert result is True

            sent_messages = [
                call.args[0] for call in mock_server.send_message.call_args_list
            ]
            assert [message["To"] for message in sent_messages] == [
                "clinic-primary@example.com",
                "clinic-secondary@example.com",
            ]
            assert all(
                message.get_content_type() == "text/plain"
                for message in sent_messages
            )
            assert all("Jane" not in message.get_content() for message in sent_messages)
            assert all(
                "https://admin-staging.drfarahvipurgentcare.com"
                in message.get_content()
                for message in sent_messages
            )
