"""Privacy-safe marketing outcome read models.

This module derives business outcomes from authoritative first-party appointment
state. It does not send data to Google or any other third party.

`visit_completed` is currently derived from Appointment.status == "completed".
The read model intentionally excludes patient identity, reason-for-visit,
service/clinical context, and other PHI/PII. Acquisition identifiers are joined
from AppointmentAttribution only when they already exist in the first-party
marketing record.
"""

from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.appointment_attribution import AppointmentAttribution


def _touch_value(touch: dict | None, key: str) -> str | None:
    if not touch:
        return None
    value = touch.get(key)
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _preferred_touch(attribution: AppointmentAttribution | None) -> dict | None:
    if attribution is None:
        return None
    return attribution.last_touch or attribution.first_touch


def build_visit_completed_rows(db: Session) -> list[dict[str, Any]]:
    """Return one deduplicated, non-clinical row per completed appointment.

    The appointment id is used only to create an opaque internal outcome key.
    The conversion timestamp is the scheduled visit start time, which is stable
    and avoids using a mutable record-updated timestamp. If the clinic later
    records an explicit completion timestamp, this contract can migrate to that
    field without changing the deduplication key.
    """

    rows = (
        db.query(Appointment, AppointmentAttribution)
        .outerjoin(
            AppointmentAttribution,
            AppointmentAttribution.appointment_id == Appointment.id,
        )
        .filter(Appointment.status == "completed")
        .order_by(Appointment.starts_at.asc(), Appointment.id.asc())
        .all()
    )

    outcomes: list[dict[str, Any]] = []
    for appointment, attribution in rows:
        touch = _preferred_touch(attribution)
        source = (
            _touch_value(touch, "source")
            or appointment.source
            or "unknown"
        )

        outcomes.append(
            {
                "outcome_key": f"visit_completed:{appointment.id}",
                "event_name": "visit_completed",
                "occurred_at": appointment.starts_at,
                "source": source,
                "gclid": _touch_value(touch, "gclid"),
                "gbraid": _touch_value(touch, "gbraid"),
                "wbraid": _touch_value(touch, "wbraid"),
                "marketing_session_id": (
                    attribution.marketing_session_id if attribution else None
                ),
                "partner_code": attribution.partner_code if attribution else None,
                "traveler_segment": (
                    attribution.traveler_segment if attribution else "unknown"
                ),
                "attribution_version": (
                    attribution.attribution_version if attribution else None
                ),
            }
        )

    return outcomes
