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


def _build_notification_body(booking: dict) -> tuple[str, str]:
    """Build plain-text and HTML notification body for clinic review."""
    subject = f"[Dr. Farah] New booking request — {booking['first_name']} {booking['last_name']}"

    body = f"""New appointment request received.

Patient: {booking['first_name']} {booking['last_name']}
Service: {booking['service_type']}
Visit:   {booking['visit_type']}
Day:     {booking['preferred_day']}
Time:    {booking['preferred_time']}
Window:  {booking.get('time_window') or 'Any'}
Reason:  {booking['reason_category']}

Contact:
  Email: {booking['email']}
  Phone: {booking['phone']}

Status:  requested

This is an automated notification — do not reply.
Review the request and follow the clinic's standard confirmation process.
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
    """Send a booking notification email to the clinic mailbox.

    Returns True if the email was sent (or test-logged), False on failure.
    Does NOT raise exceptions — failures are logged, not propagated.
    """
    subject, body = _build_notification_body(booking)
    return _send_email_message(settings.SMTP_TO, subject, body)
