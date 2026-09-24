"""Tests for privacy-safe transactional email delivery.

All provider calls are mocked; no real email is sent.
"""

import importlib
import os
from unittest.mock import MagicMock, patch
from uuid import UUID

import httpx
import pytest


EMAIL_ENV_KEYS = (
    "EMAIL_TRANSPORT",
    "EMAIL_FROM_NAME",
    "EMAIL_TIMEOUT_SECONDS",
    "EMAIL_MAX_ATTEMPTS",
    "BREVO_API_URL",
    "BREVO_API_KEY",
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USER",
    "SMTP_PASSWORD",
    "SMTP_FROM",
    "SMTP_TO",
    "SMTP_USE_TLS",
    "SMTP_TEST_MODE",
    "ADMIN_PORTAL_URL",
)


@pytest.fixture(autouse=True)
def clean_email_env():
    """Provide deterministic email settings and restore the environment."""
    saved = {key: os.environ.get(key) for key in EMAIL_ENV_KEYS}
    for key in EMAIL_ENV_KEYS:
        os.environ.pop(key, None)

    os.environ.update(
        {
            "EMAIL_TRANSPORT": "smtp",
            "EMAIL_FROM_NAME": "Dr. Farah VIP Urgent Care",
            "EMAIL_TIMEOUT_SECONDS": "20",
            "EMAIL_MAX_ATTEMPTS": "3",
            "BREVO_API_URL": "https://api.brevo.com/v3/smtp/email",
            "BREVO_API_KEY": "",
            "SMTP_HOST": "smtp-relay.brevo.com",
            "SMTP_PORT": "587",
            "SMTP_USER": "test-login@smtp-brevo.com",
            "SMTP_PASSWORD": "test-smtp-password",
            "SMTP_FROM": "notifications@drfarahvipurgentcare.com",
            "SMTP_TO": (
                "clinic-primary@example.com,clinic-secondary@example.com"
            ),
            "SMTP_USE_TLS": "true",
            "SMTP_TEST_MODE": "false",
            "ADMIN_PORTAL_URL": (
                "https://admin-staging.drfarahvipurgentcare.com"
            ),
        }
    )

    from app.core.config import get_settings

    get_settings.cache_clear()
    import app.services.email

    importlib.reload(app.services.email)
    yield

    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
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


def _response(status_code: int, body: dict | None = None) -> httpx.Response:
    return httpx.Response(
        status_code,
        json=body or {},
        request=httpx.Request(
            "POST", "https://api.brevo.com/v3/smtp/email"
        ),
    )


class TestBrevoApiTransport:
    def _enable_api(self):
        from app.services.email import settings

        settings.EMAIL_TRANSPORT = "brevo_api"
        settings.BREVO_API_KEY = "test-api-key"

    def test_success_returns_true_and_uses_privacy_safe_payload(self):
        self._enable_api()
        from app.services.email import _send_email_message

        with patch("app.services.email.httpx.post") as mock_post:
            mock_post.return_value = _response(
                201, {"messageId": "provider-message-id"}
            )

            result = _send_email_message(
                "clinic@example.com",
                "Generic notification",
                "No patient information.",
                "<p>No patient information.</p>",
            )

        assert result is True
        kwargs = mock_post.call_args.kwargs
        assert kwargs["timeout"] == 20.0
        assert kwargs["headers"]["api-key"] == "test-api-key"
        payload = kwargs["json"]
        assert payload["sender"] == {
            "name": "Dr. Farah VIP Urgent Care",
            "email": "notifications@drfarahvipurgentcare.com",
        }
        assert payload["to"] == [{"email": "clinic@example.com"}]
        assert payload["textContent"] == "No patient information."
        assert payload["htmlContent"] == "<p>No patient information.</p>"
        UUID(payload["headers"]["idempotencyKey"])
        assert "test-api-key" not in repr(payload)

    def test_transient_responses_retry_with_same_idempotency_key(self):
        self._enable_api()
        from app.services.email import _send_email_message

        with (
            patch("app.services.email.httpx.post") as mock_post,
            patch("app.services.email.time.sleep") as mock_sleep,
        ):
            mock_post.side_effect = [
                _response(500),
                _response(429),
                _response(201, {"messageId": "accepted-after-retry"}),
            ]

            result = _send_email_message(
                "clinic@example.com", "Subject", "Body"
            )

        assert result is True
        assert mock_post.call_count == 3
        keys = [
            call.kwargs["json"]["headers"]["idempotencyKey"]
            for call in mock_post.call_args_list
        ]
        assert len(set(keys)) == 1
        assert mock_sleep.call_args_list[0].args == (1,)
        assert mock_sleep.call_args_list[1].args == (2,)

    def test_network_failure_retries_then_succeeds(self):
        self._enable_api()
        from app.services.email import _send_email_message

        request = httpx.Request(
            "POST", "https://api.brevo.com/v3/smtp/email"
        )
        with (
            patch("app.services.email.httpx.post") as mock_post,
            patch("app.services.email.time.sleep"),
        ):
            mock_post.side_effect = [
                httpx.ConnectTimeout("timeout", request=request),
                _response(201, {"messageId": "accepted"}),
            ]
            assert (
                _send_email_message(
                    "clinic@example.com", "Subject", "Body"
                )
                is True
            )
        assert mock_post.call_count == 2

    def test_duplicate_after_lost_response_counts_as_accepted(self):
        self._enable_api()
        from app.services.email import _send_email_message

        request = httpx.Request(
            "POST", "https://api.brevo.com/v3/smtp/email"
        )
        with (
            patch("app.services.email.httpx.post") as mock_post,
            patch("app.services.email.time.sleep"),
        ):
            mock_post.side_effect = [
                httpx.ReadTimeout("response lost", request=request),
                _response(400, {"code": "duplicate_parameter"}),
            ]
            assert (
                _send_email_message(
                    "clinic@example.com", "Subject", "Body"
                )
                is True
            )

        assert mock_post.call_count == 2
        keys = [
            call.kwargs["json"]["headers"]["idempotencyKey"]
            for call in mock_post.call_args_list
        ]
        assert len(set(keys)) == 1

    def test_authentication_error_does_not_retry_or_log_key(self, caplog):
        self._enable_api()
        from app.services.email import _send_email_message

        with patch("app.services.email.httpx.post") as mock_post:
            mock_post.return_value = _response(401)
            result = _send_email_message(
                "clinic@example.com", "Subject", "Body"
            )

        assert result is False
        assert mock_post.call_count == 1
        assert "test-api-key" not in caplog.text

    def test_missing_api_key_fails_closed(self):
        self._enable_api()
        from app.services.email import _send_email_message, settings

        settings.BREVO_API_KEY = ""
        with patch("app.services.email.httpx.post") as mock_post:
            assert (
                _send_email_message(
                    "clinic@example.com", "Subject", "Body"
                )
                is False
            )
        mock_post.assert_not_called()


class TestSmtpRollbackTransport:
    def test_successful_send(self):
        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_server = MagicMock()
            mock_smtp.return_value.__enter__.return_value = mock_server

            result = send_booking_notification(BOOKING_DATA)

        assert result is True
        assert mock_smtp.call_count == 2
        mock_smtp.assert_any_call(
            "smtp-relay.brevo.com", 587, timeout=20.0
        )
        assert mock_server.starttls.call_count == 2
        assert mock_server.login.call_count == 2
        assert mock_server.send_message.call_count == 2

    def test_smtp_failure_does_not_expose_secret(self, caplog):
        from app.services.email import send_booking_notification

        with patch("app.services.email.smtplib.SMTP") as mock_smtp:
            mock_smtp.side_effect = ConnectionRefusedError(
                "Connection refused"
            )
            assert send_booking_notification(BOOKING_DATA) is False

        assert "test-smtp-password" not in caplog.text


class TestEmailConfigurationAndPrivacy:
    def test_test_mode_avoids_all_provider_calls(self):
        from app.services.email import _send_email_message, settings

        settings.SMTP_TEST_MODE = True
        settings.EMAIL_TRANSPORT = "brevo_api"
        with (
            patch("app.services.email.httpx.post") as mock_post,
            patch("app.services.email.smtplib.SMTP") as mock_smtp,
        ):
            assert (
                _send_email_message(
                    "clinic@example.com", "Subject", "Body"
                )
                is True
            )
        mock_post.assert_not_called()
        mock_smtp.assert_not_called()

    def test_recipient_list_trims_and_deduplicates(self):
        from app.services.email import settings

        settings.SMTP_TO = (
            " clinic-primary@example.com,clinic-secondary@example.com,"
            "clinic-primary@example.com, "
        )
        assert settings.smtp_to_list == [
            "clinic-primary@example.com",
            "clinic-secondary@example.com",
        ]

    def test_subject_and_body_exclude_booking_details(self):
        from app.services.email import _build_notification_body

        subject, body = _build_notification_body(BOOKING_DATA)
        for sensitive_value in BOOKING_DATA.values():
            if sensitive_value:
                assert str(sensitive_value) not in subject
                assert str(sensitive_value) not in body
        assert "Dr. Farah" in subject
        assert "no patient or appointment details" in body.lower()
        assert (
            "https://admin-staging.drfarahvipurgentcare.com" in body
        )

    def test_no_recipients_returns_false_without_provider_call(self):
        from app.services.email import send_booking_notification, settings

        settings.SMTP_TO = " , "
        with (
            patch("app.services.email.httpx.post") as mock_post,
            patch("app.services.email.smtplib.SMTP") as mock_smtp,
        ):
            assert send_booking_notification(BOOKING_DATA) is False
        mock_post.assert_not_called()
        mock_smtp.assert_not_called()
