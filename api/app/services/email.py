"""Minimal email notification service.

Uses SMTP environment variables from K8s secrets.
When SMTP_TEST_MODE=true, emails are logged instead of sent.

No credentials appear in logs.
"""

import logging
import smtplib
from email.message import EmailMessage

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


def _build_notification_body(_booking: dict) -> tuple[str, str]:
    """Build a privacy-preserving notification for clinic review.

    The booking payload is intentionally not interpolated into the message.
    Appointment and patient details remain in the authenticated admin portal.
    """
    subject = "[Dr. Farah] New appointment request received"

    body = f"""A new appointment request has been received.

For privacy, no patient or appointment details are included in this email.

Review the request in the secure admin portal:
{settings.ADMIN_PORTAL_URL}

This is an automated notification — do not reply.
"""

    return subject, body


def _send_email_message(
    to_email: str, subject: str, text_body: str, html_body: str | None = None
) -> bool:
    """Low-level send — one email, one recipient. Respects SMTP_TEST_MODE.

    When html_body is given the message is sent as multipart/alternative
    (text/plain + text/html).  Otherwise it is plain-text only.

    Returns True if the email was sent (or test-logged), False on failure.
    Does NOT raise exceptions.
    """
    if not settings.SMTP_HOST:
        logger.warning("SMTP not configured — skipping email.")
        return False

    if settings.SMTP_TEST_MODE:
        logger.info(
            "SMTP TEST MODE — would send: subject=%r to=%s", subject, to_email
        )
        return True

    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = to_email
        msg.set_content(text_body)
        if html_body:
            msg.add_alternative(html_body, subtype="html")

        port = settings.SMTP_PORT

        with smtplib.SMTP(settings.SMTP_HOST, port, timeout=15) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Email sent: subject=%r to=%s", subject, to_email)
        return True

    except Exception:
        logger.exception("Failed to send email — subject=%r", subject)
        return False


def send_booking_notification(booking: dict) -> bool:
    """Send a separate booking notification to each clinic mailbox.

    Separate messages keep recipient addresses private from one another and let
    delivery continue when one mailbox fails. Returns True only when at least
    one recipient exists and every delivery succeeds (or is test-logged).
    """
    subject, body = _build_notification_body(booking)
    recipients = settings.smtp_to_list
    if not recipients:
        logger.warning("No clinic notification recipients configured.")
        return False

    results = [
        _send_email_message(recipient, subject, body) for recipient in recipients
    ]
    return all(results)
