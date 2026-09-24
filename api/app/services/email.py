"""Privacy-safe transactional email delivery.

Brevo's HTTPS API is the preferred transport. The API key stays in a
Kubernetes Secret and is never logged. SMTP is retained only as an explicit
compatibility/rollback transport.
"""

import logging
import smtplib
import ssl
import time
from email.message import EmailMessage
from uuid import uuid4

import httpx

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _build_notification_body(_booking: dict) -> tuple[str, str]:
    """Build a privacy-preserving notification for clinic review."""
    subject = "[Dr. Farah] New appointment request received"

    body = f"""A new appointment request has been received.

For privacy, no patient or appointment details are included in this email.

Review the request in the secure admin portal:
{settings.ADMIN_PORTAL_URL}

This is an automated notification — do not reply.
"""

    return subject, body


def _brevo_payload(
    to_email: str,
    subject: str,
    text_body: str,
    html_body: str | None,
    idempotency_key: str,
) -> dict:
    payload: dict = {
        "sender": {
            "name": settings.EMAIL_FROM_NAME,
            "email": settings.SMTP_FROM,
        },
        "to": [{"email": to_email}],
        "subject": subject,
        "textContent": text_body,
        # Brevo reuses this UUID during retries and rejects duplicate sends.
        "headers": {"idempotencyKey": idempotency_key},
    }
    if html_body:
        payload["htmlContent"] = html_body
    return payload


def _send_via_brevo_api(
    to_email: str, subject: str, text_body: str, html_body: str | None
) -> bool:
    if not settings.BREVO_API_KEY or not settings.SMTP_FROM:
        logger.error("Brevo API email transport is not configured.")
        return False

    idempotency_key = str(uuid4())
    payload = _brevo_payload(
        to_email, subject, text_body, html_body, idempotency_key
    )
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": settings.BREVO_API_KEY,
    }

    for attempt in range(1, settings.EMAIL_MAX_ATTEMPTS + 1):
        try:
            response = httpx.post(
                settings.BREVO_API_URL,
                headers=headers,
                json=payload,
                timeout=settings.EMAIL_TIMEOUT_SECONDS,
            )

            # If the first request was accepted but its response was lost, a
            # retry with the same UUID is rejected as a duplicate. That means
            # Brevo already processed the original message.
            if response.status_code == 400:
                try:
                    error_code = response.json().get("code")
                except ValueError:
                    error_code = None
                if error_code == "duplicate_parameter":
                    logger.info(
                        "Brevo API confirmed an idempotent duplicate — "
                        "subject=%r",
                        subject,
                    )
                    return True

            if response.status_code == 429 or response.status_code >= 500:
                if attempt < settings.EMAIL_MAX_ATTEMPTS:
                    logger.warning(
                        "Transient Brevo API failure — status=%s attempt=%s/%s",
                        response.status_code,
                        attempt,
                        settings.EMAIL_MAX_ATTEMPTS,
                    )
                    time.sleep(2 ** (attempt - 1))
                    continue

            response.raise_for_status()
            data = response.json()
            logger.info(
                "Email accepted by Brevo API — subject=%r message_id=%s",
                subject,
                data.get("messageId", "unknown"),
            )
            return True

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Brevo API rejected email — status=%s subject=%r",
                exc.response.status_code,
                subject,
            )
            return False
        except httpx.RequestError as exc:
            if attempt < settings.EMAIL_MAX_ATTEMPTS:
                logger.warning(
                    "Brevo API connection failure — type=%s attempt=%s/%s",
                    type(exc).__name__,
                    attempt,
                    settings.EMAIL_MAX_ATTEMPTS,
                )
                time.sleep(2 ** (attempt - 1))
                continue
            logger.error(
                "Brevo API connection failed after retries — type=%s subject=%r",
                type(exc).__name__,
                subject,
            )
            return False

    return False


def _send_via_smtp(
    to_email: str, subject: str, text_body: str, html_body: str | None
) -> bool:
    if not settings.SMTP_HOST:
        logger.error("SMTP email transport is not configured.")
        return False

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = settings.SMTP_FROM
    msg["To"] = to_email
    msg.set_content(text_body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT,
        timeout=settings.EMAIL_TIMEOUT_SECONDS,
    ) as server:
        if settings.SMTP_USE_TLS:
            server.starttls(context=ssl.create_default_context())
        if settings.SMTP_USER and settings.SMTP_PASSWORD:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        server.send_message(msg)

    logger.info("Email accepted by SMTP relay — subject=%r", subject)
    return True


def _send_email_message(
    to_email: str, subject: str, text_body: str, html_body: str | None = None
) -> bool:
    """Send one privacy-safe message using the configured transport.

    Returns True only when the provider accepts the message. Credentials and
    message bodies are never logged. Provider failures never escape to booking
    handlers, which continue to preserve the already-created appointment.
    """
    if settings.SMTP_TEST_MODE:
        logger.info("EMAIL TEST MODE — would send: subject=%r", subject)
        return True

    transport = settings.EMAIL_TRANSPORT.strip().lower()
    try:
        if transport == "brevo_api":
            return _send_via_brevo_api(
                to_email, subject, text_body, html_body
            )
        if transport == "smtp":
            return _send_via_smtp(to_email, subject, text_body, html_body)

        logger.error("Unsupported email transport: %r", transport)
        return False
    except Exception as exc:
        logger.error(
            "Failed to send email — transport=%s type=%s subject=%r",
            transport,
            type(exc).__name__,
            subject,
        )
        return False


def send_booking_notification(booking: dict) -> bool:
    """Send a separate booking notification to each clinic mailbox."""
    subject, body = _build_notification_body(booking)
    recipients = settings.smtp_to_list
    if not recipients:
        logger.warning("No clinic notification recipients configured.")
        return False

    results = [
        _send_email_message(recipient, subject, body) for recipient in recipients
    ]
    return all(results)
