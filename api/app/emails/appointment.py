"""Appointment confirmation email templates.

Two emails per appointment:
  1. Patient confirmation — warm, reassuring, includes reference + PT time
  2. Clinic notification — concise, includes patient contact details

When SMTP_TEST_MODE=true, emails are logged instead of sent.
"""

import logging
from zoneinfo import ZoneInfo

from app.services.email import _send_email_message
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

PACIFIC = ZoneInfo("America/Los_Angeles")
CLINIC_PHONE = "310-467-0101"


# ---------------------------------------------------------------------------
# Template builders
# ---------------------------------------------------------------------------

def build_patient_confirmation(appt, service_name: str) -> tuple[str, str, str]:
    """Build patient confirmation email.

    Returns (subject, text_body, html_body).
    """
    pt = appt.starts_at.astimezone(PACIFIC)
    when = pt.strftime("%A, %B %d, %Y at %I:%M %p PT")

    subject = "Your appointment request — Dr. Farah"

    text = (
        f"Dear {appt.first_name},\n\n"
        f"We've received your appointment request.\n\n"
        f"Service:   {service_name}\n"
        f"When:      {when}\n"
        f"Reference: {appt.id}\n\n"
        f"If you need to change anything, call {CLINIC_PHONE}.\n\n"
        f"In an emergency, call 911.\n\n"
        f"— Dr. Farah VIP Urgent Care\n"
    )

    html = (
        f"<p>Dear {appt.first_name},</p>\n"
        f"<p>We've received your appointment request.</p>\n"
        f"<table style='border-collapse:collapse;'>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Service</td>"
        f"<td style='padding:4px 0;'>{service_name}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>When</td>"
        f"<td style='padding:4px 0;'>{when}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Reference</td>"
        f"<td style='padding:4px 0;'>{appt.id}</td></tr>\n"
        f"</table>\n"
        f"<p>If you need to change anything, call {CLINIC_PHONE}.</p>\n"
        f"<p>In an emergency, call 911.</p>\n"
        f"<p>— Dr. Farah VIP Urgent Care</p>\n"
    )

    return subject, text, html


def build_clinic_notification(appt, service_name: str) -> tuple[str, str, str]:
    """Build clinic notification email.

    Returns (subject, text_body, html_body).
    """
    pt = appt.starts_at.astimezone(PACIFIC)
    when = pt.strftime("%A, %B %d, %Y at %I:%M %p PT")

    subject = f"New appointment request — {appt.first_name} {appt.last_name}"

    text = (
        f"New appointment request received.\n\n"
        f"Patient:   {appt.first_name} {appt.last_name}\n"
        f"Service:   {service_name}\n"
        f"When:      {when}\n"
        f"Reason:    {appt.reason_category}\n"
        f"Reference: {appt.id}\n"
        f"Status:    {appt.status}\n\n"
        f"Contact:\n"
        f"  Email: {appt.email}\n"
        f"  Phone: {appt.phone}\n\n"
        f"This is an automated notification.\n"
    )

    html = (
        f"<p><strong>New appointment request received.</strong></p>\n"
        f"<table style='border-collapse:collapse;'>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Patient</td>"
        f"<td style='padding:4px 0;'>{appt.first_name} {appt.last_name}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Service</td>"
        f"<td style='padding:4px 0;'>{service_name}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>When</td>"
        f"<td style='padding:4px 0;'>{when}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Reason</td>"
        f"<td style='padding:4px 0;'>{appt.reason_category}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Reference</td>"
        f"<td style='padding:4px 0;'>{appt.id}</td></tr>\n"
        f"<tr><td style='padding:4px 12px 4px 0;font-weight:bold;'>Status</td>"
        f"<td style='padding:4px 0;'>{appt.status}</td></tr>\n"
        f"</table>\n"
        f"<p>Email: {appt.email}<br>Phone: {appt.phone}</p>\n"
        f"<p><em>This is an automated notification.</em></p>\n"
    )

    return subject, text, html


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def send_appointment_emails(appt, service_name: str) -> None:
    """Send confirmation to patient and notification to clinic.

    Best-effort only — each send is individually wrapped so one failure
    does not prevent the other. This function NEVER raises.
    """
    # Patient confirmation
    try:
        subj, text, html = build_patient_confirmation(appt, service_name)
        _send_email_message(appt.email, subj, html if html else text)
    except Exception:
        logger.warning("Failed to send patient confirmation for appointment %s", appt.id)

    # Clinic notification
    try:
        subj, text, html = build_clinic_notification(appt, service_name)
        _send_email_message(settings.SMTP_FROM, subj, html if html else text)
    except Exception:
        logger.warning("Failed to send clinic notification for appointment %s", appt.id)
