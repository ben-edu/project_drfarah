"""Tests for the email notification service.

Uses mocks — no real email is ever sent.
"""

import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def clean_smtp_env():
    """Ensure a clean SMTP environment for each test."""
    saved = {}
    for k in (
        "SMTP_HOST", "SMTP_PORT", "SMTP_USER", "SMTP_PASSWORD",
        "SMTP_FROM", "SMTP_TO", "SMTP_USE_TLS", "SMTP_TEST_MODE",
    ):
        saved[k] = os.environ.get(k)
    for k in saved:
        os.environ.pop(k, None)
    os.environ["SMTP_HOST"] = "mail.soria-academie.fr"
    os.environ["SMTP_PORT"] = "587"
    os.environ["SMTP_USER"] = "contact@soria-academie.fr"
    os.environ["SMTP_PASSWORD"] = "test-password"
    os.environ["SMTP_FROM"] = "contact@soria-academie.fr"
    os.environ["SMTP_TO"] = "appointments@drfarah.proxbenovh.cloud"
    os.environ["SMTP_USE_TLS"] = "true"
    os.environ["SMTP_TEST_MODE"] = "false"

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


BOOKING_DATA = {
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


class TestEmailNotification:
    def test_successful_send(self, clean_smtp_env):
        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = send_booking_notification(BOOKING_DATA)

            assert result is True
            mock_smtp.assert_called_once_with("mail.soria-academie.fr", 587, timeout=15)
            mock_server.starttls.assert_called_once()
            mock_server.login.assert_called_once_with("contact@soria-academie.fr", "test-password")
            mock_server.send_message.assert_called_once()

    def test_sender_address_is_correct(self, clean_smtp_env):
        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            send_booking_notification(BOOKING_DATA)

            sent_msg = mock_server.send_message.call_args[0][0]
            assert sent_msg["From"] == "contact@soria-academie.fr"
            assert sent_msg["To"] == "appointments@drfarah.proxbenovh.cloud"

    def test_no_secrets_in_log_on_failure(self, clean_smtp_env, capsys):
        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = ConnectionRefusedError("Connection refused")

            result = send_booking_notification(BOOKING_DATA)

            assert result is False

        # Check that the secret password did not appear in logs
        captured = capsys.readouterr()
        assert "test-password" not in captured.out
        assert "test-password" not in captured.err

    def test_test_mode_logs_instead_of_sending(self, clean_smtp_env):
        os.environ["SMTP_TEST_MODE"] = "true"
        from app.core.config import get_settings
        get_settings.cache_clear()

        import importlib
        import app.services.email
        importlib.reload(app.services.email)

        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            result = send_booking_notification(BOOKING_DATA)
            assert result is True
            mock_smtp.assert_not_called()

    def test_subject_contains_patient_name(self, clean_smtp_env):
        from app.services.email import _build_notification_body

        subject, body = _build_notification_body(BOOKING_DATA)
        assert "Jane" in subject
        assert "Doe" in subject
        assert "Dr. Farah" in subject

    def test_body_does_not_contain_clinical_free_text(self, clean_smtp_env):
        from app.services.email import _build_notification_body

        subject, body = _build_notification_body(BOOKING_DATA)
        # Body contains structured booking data only.
        assert "Urgent or acute care" in body
        assert "jane@example.com" in body
        assert "+1-310-555-0189" in body
        # No clinical free text fields exist.
        assert "symptoms" not in body.lower()
        assert "diagnosis" not in body.lower()
        assert "medication" not in body.lower()

    def test_smtp_not_configured_returns_false(self):
        os.environ["SMTP_HOST"] = ""
        from app.core.config import get_settings
        get_settings.cache_clear()

        import importlib
        import app.services.email
        importlib.reload(app.services.email)

        from app.services.email import send_booking_notification

        result = send_booking_notification(BOOKING_DATA)
        assert result is False
