"""Privacy-preserving appointment email templates.

Privacy-safe transactional emails:
  1. Patient acknowledgement — confirms receipt without appointment details
  2. Clinic notification — directs staff to the authenticated admin portal
  3. Patient status notification — confirms or cancels without appointment details

When SMTP_TEST_MODE=true, emails are logged instead of sent.
"""

import logging

from app.services.email import _send_email_message
from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

CLINIC_PHONE = "310-467-0101"


# ---------------------------------------------------------------------------
# Template builders
# ---------------------------------------------------------------------------

def build_patient_confirmation(appt, service_name: str) -> tuple[str, str, str]:
    """Build a generic patient acknowledgement without appointment details.

    Returns (subject, text_body, html_body).
    """
    # Keep the existing call signature while deliberately excluding both
    # objects from the email body. Details remain in the application database.
    _ = (appt, service_name)

    subject = "Your appointment request — Dr. Farah"

    text = (
        "Hello,\n\n"
        "We've received your appointment request. It is not confirmed until "
        "the clinic contacts you.\n\n"
        "For your privacy, appointment details are not included in this email.\n\n"
        f"If you need to change anything, call {CLINIC_PHONE}.\n\n"
        "In an emergency, call 911.\n\n"
        "— Dr. Farah VIP Urgent Care\n"
    )

    html = (
        '<div style="max-width:600px;margin:0 auto;font-family:'
        '-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,'
        'Arial,sans-serif;color:#1a1a2e;line-height:1.6;">\n'
        "<p>Hello,</p>\n"
        "<p>We've received your appointment request. It is not confirmed until "
        "the clinic contacts you.</p>\n"
        "<p>For your privacy, appointment details are not included in this email.</p>\n"
        f"<p>If you need to change anything, call {CLINIC_PHONE}.</p>\n"
        "<p>In an emergency, call 911.</p>\n"
        "<p style='color:#6b7280;'>— Dr. Farah VIP Urgent Care</p>\n"
        "</div>\n"
    )

    return subject, text, html


def build_patient_status_notification(status: str) -> tuple[str, str, str]:
    """Build a privacy-safe confirmation or cancellation email.

    Only the status outcome is included. Appointment, patient, service, and
    scheduling details remain in the application database.

    Returns (subject, text_body, html_body).
    """
    if status == "confirmed":
        subject = "Your appointment is confirmed — Dr. Farah"
        outcome = "Your appointment request has been confirmed by the clinic."
        next_step = (
            f"If you need to change or cancel it, call {CLINIC_PHONE}."
        )
    elif status == "cancelled":
        subject = "Your appointment has been cancelled — Dr. Farah"
        outcome = "Your appointment has been cancelled."
        next_step = (
            f"If this was unexpected or you want another appointment, "
            f"call {CLINIC_PHONE}."
        )
    else:
        raise ValueError(
            "Patient status notifications support only confirmed or cancelled"
        )

    text = (
        "Hello,\n\n"
        f"{outcome}\n\n"
        "For your privacy, appointment details are not included in this email.\n\n"
        f"{next_step}\n\n"
        "In an emergency, call 911.\n\n"
        "— Dr. Farah VIP Urgent Care\n"
    )

    html = (
        '<div style="max-width:600px;margin:0 auto;font-family:'
        "-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,"
        'Arial,sans-serif;color:#1a1a2e;line-height:1.6;">\n'
        "<p>Hello,</p>\n"
        f"<p>{outcome}</p>\n"
        "<p>For your privacy, appointment details are not included in this email.</p>\n"
        f"<p>{next_step}</p>\n"
        "<p>In an emergency, call 911.</p>\n"
        "<p style='color:#6b7280;'>— Dr. Farah VIP Urgent Care</p>\n"
        "</div>\n"
    )

    return subject, text, html


def build_clinic_notification(appt, service_name: str) -> tuple[str, str, str]:
    """Build a generic clinic notification without patient details.

    Returns (subject, text_body, html_body).
    """
    _ = (appt, service_name)

    subject = "New appointment request — Dr. Farah"

    text = (
        "A new appointment request has been received.\n\n"
        "For privacy, no patient or appointment details are included in this email.\n\n"
        "Review the request in the secure admin portal:\n"
        f"{settings.ADMIN_PORTAL_URL}\n\n"
        "This is an automated notification — do not reply.\n"
    )

    html = (
        '<div style="max-width:600px;margin:0 auto;font-family:'
        '-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,'
        'Arial,sans-serif;color:#1a1a2e;line-height:1.6;">\n'
        "<p><strong>A new appointment request has been received.</strong></p>\n"
        "<p>For privacy, no patient or appointment details are included in this email.</p>\n"
        f"<p><a href='{settings.ADMIN_PORTAL_URL}'>Review it in the secure admin portal</a>.</p>\n"
        "<p style='color:#6b7280;'><em>This is an automated notification — "
        "do not reply.</em></p>\n"
        "</div>\n"
    )

    return subject, text, html


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def send_patient_status_notification(appt, new_status: str) -> bool:
    """Notify the patient of a confirmed or cancelled appointment.

    Delivery is best-effort and this function never raises. A False result
    means the status update remains valid but the message was not accepted.
    """
    try:
        subject, text, html = build_patient_status_notification(new_status)
        accepted = _send_email_message(appt.email, subject, text, html)
    except Exception:
        logger.exception(
            "Failed to send %s notification for appointment %s",
            new_status,
            appt.id,
        )
        return False

    if not accepted:
        logger.warning(
            "%s notification was not accepted for appointment %s",
            new_status.capitalize(),
            appt.id,
        )
        return False

    return True


def send_appointment_emails(appt, service_name: str) -> None:
    """Send confirmation to patient and notification to clinic.

    Best-effort only — each send is individually wrapped so one failure
    does not prevent the other. This function NEVER raises.
    """
    # Patient confirmation
    try:
        subj, text, html = build_patient_confirmation(appt, service_name)
        _send_email_message(appt.email, subj, text, html)
    except Exception:
        logger.warning("Failed to send patient confirmation for appointment %s", appt.id)

    # Clinic notifications are sent separately so recipient addresses stay
    # private and a failed mailbox does not block the remaining recipients.
    subj, text, html = build_clinic_notification(appt, service_name)
    recipients = settings.smtp_to_list
    if not recipients:
        logger.warning("No clinic notification recipients configured.")

    for recipient in recipients:
        try:
            _send_email_message(recipient, subj, text, html)
        except Exception:
            logger.warning(
                "Failed to send clinic notification for appointment %s", appt.id
            )
