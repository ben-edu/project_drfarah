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


def send_booking_notification(booking: dict) -> bool:
    """Send a booking notification email to the clinic mailbox.

    Returns True if the email was sent (or test-logged), False on failure.
    Does NOT raise exceptions — failures are logged, not propagated.
    """
    if not settings.SMTP_HOST:
        logger.warning("SMTP not configured — skipping booking notification.")
        return False

    if settings.SMTP_TEST_MODE:
        subject, body = _build_notification_body(booking)
        logger.info(
            "SMTP TEST MODE — would send: subject=%r recipient=%s", subject, settings.SMTP_TO
        )
        return True

    try:
        subject, body = _build_notification_body(booking)

        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = settings.SMTP_FROM
        msg["To"] = settings.SMTP_TO
        msg.set_content(body)

        if settings.SMTP_USE_TLS:
            context = None
            port = settings.SMTP_PORT
        else:
            context = None
            port = settings.SMTP_PORT

        with smtplib.SMTP(settings.SMTP_HOST, port, timeout=15) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)

        logger.info("Booking notification sent for %s %s", booking.get("first_name"), booking.get("last_name"))
        return True

    except Exception:
        logger.exception("Failed to send booking notification — request was saved")
        return False
