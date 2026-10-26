"""Appointment scheduling endpoints.

GET  /api/v1/services            — list active services
GET  /api/v1/availability        — available appointment slots
POST /api/v1/appointments        — create a scheduled appointment
POST /api/v1/internal/cleanup-ci — clean up CI smoke-test records (token-protected)
"""

import datetime
import logging
from secrets import compare_digest

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.emails.appointment import send_appointment_emails
from app.models.appointment import Appointment
from app.models.appointment_attribution import AppointmentAttribution
from app.models.service import Service
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.schemas.availability import (
    AvailabilityResponse,
    AvailabilityServiceInfo,
    SlotOut,
)
from app.schemas.service import ServiceListResponse, ServiceOut
from app.services import scheduling

logger = logging.getLogger(__name__)
router = APIRouter(tags=["appointments"])
settings = get_settings()


@router.get("/services", response_model=ServiceListResponse)
def list_services(db: Session = Depends(get_db)):
    """List active services available for booking."""
    services = (
        db.query(Service)
        .filter(Service.is_active == True)
        .order_by(Service.name)
        .all()
    )
    return ServiceListResponse(
        services=[ServiceOut.model_validate(s) for s in services]
    )


@router.get("/availability", response_model=AvailabilityResponse)
def get_availability(
    service_code: str = Query(..., min_length=1, max_length=64),
    start_date: str = Query(..., min_length=10, max_length=10),
    end_date: str = Query(..., min_length=10, max_length=10),
    db: Session = Depends(get_db),
):
    """Return available appointment slots for a service and date range."""
    service = (
        db.query(Service)
        .filter(Service.code == service_code, Service.is_active == True)
        .first()
    )
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        sd = datetime.date.fromisoformat(start_date)
        ed = datetime.date.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format — use YYYY-MM-DD")

    if sd > ed:
        raise HTTPException(status_code=422, detail="start_date must not be after end_date")

    if (ed - sd).days > scheduling.MAX_AVAILABILITY_DAYS:
        raise HTTPException(
            status_code=422,
            detail=f"Date range must not exceed {scheduling.MAX_AVAILABILITY_DAYS} days",
        )

    slots = scheduling.generate_availability(db, service, sd, ed)

    return AvailabilityResponse(
        service=AvailabilityServiceInfo(
            code=service.code,
            name=service.name,
            duration_minutes=service.duration_minutes,
        ),
        timezone="America/Los_Angeles",
        slots=[SlotOut(**s) for s in slots],
    )


def _structured_source(payload: AppointmentCreate) -> str | None:
    """Return the strongest compact source while preserving CI semantics."""
    # The legacy reserved CI marker is operational metadata used to suppress
    # smoke-test email and cleanup the record. Never let nested attribution
    # replace it after the request has passed the CI authorization guard.
    if payload.source == "ci":
        return "ci"
    if payload.attribution:
        for touch in (payload.attribution.last_touch, payload.attribution.first_touch):
            if touch and touch.source:
                return touch.source[:32]
    return payload.source[:32] if payload.source else None


def _requested_reserved_ci_source(payload: AppointmentCreate) -> bool:
    """Do not allow nested attribution to bypass the reserved CI marker guard."""
    if payload.source == "ci":
        return True
    if not payload.attribution:
        return False
    return any(
        touch is not None and touch.source == "ci"
        for touch in (payload.attribution.first_touch, payload.attribution.last_touch)
    )


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
    ci_token: str | None = Header(None, alias="X-CI-Token"),
):
    """Create a scheduled appointment and optional non-clinical attribution."""
    if _requested_reserved_ci_source(payload) and not (
        settings.ENVIRONMENT == "staging"
        and settings.CLEANUP_TOKEN
        and ci_token
        and compare_digest(ci_token, settings.CLEANUP_TOKEN)
    ):
        raise HTTPException(status_code=403, detail="Reserved appointment source")

    service = (
        db.query(Service)
        .filter(Service.code == payload.service_code, Service.is_active == True)
        .first()
    )
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    try:
        starts_at = datetime.datetime.fromisoformat(payload.starts_at)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid starts_at format — use ISO 8601")

    if starts_at.tzinfo is None:
        raise HTTPException(
            status_code=422, detail="starts_at must include a timezone offset"
        )
    starts_at_utc = starts_at.astimezone(datetime.timezone.utc)

    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if starts_at_utc <= now_utc:
        raise HTTPException(status_code=422, detail="Slot is in the past")

    if not scheduling.validate_slot_in_working_hours(db, starts_at_utc, service):
        raise HTTPException(status_code=422, detail="Slot is outside working hours")

    duration = datetime.timedelta(minutes=service.duration_minutes)
    buffer_before = datetime.timedelta(minutes=service.buffer_before_minutes)
    buffer_after = datetime.timedelta(minutes=service.buffer_after_minutes)
    occ_start = starts_at_utc - buffer_before
    occ_end = starts_at_utc + duration + buffer_after

    from app.models.blocked_period import BlockedPeriod
    blocked = (
        db.query(BlockedPeriod)
        .filter(
            BlockedPeriod.is_active == True,
            BlockedPeriod.starts_at < occ_end,
            BlockedPeriod.ends_at > occ_start,
        )
        .first()
    )
    if blocked is not None:
        raise HTTPException(status_code=409, detail="Slot is blocked")

    if scheduling.check_slot_conflict(db, service, starts_at_utc):
        raise HTTPException(status_code=409, detail="Slot is no longer available")

    ends_at_utc = starts_at_utc + duration
    effective_source = _structured_source(payload)

    appointment = Appointment(
        service_id=service.id,
        starts_at=starts_at_utc,
        ends_at=ends_at_utc,
        timezone="America/Los_Angeles",
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        reason_category=payload.reason_category,
        status="pending",
        source=effective_source,
    )

    try:
        db.add(appointment)
        # Flush first so the 1:1 attribution record can reference appointment.id,
        # while keeping both records inside the same transaction.
        db.flush()

        if payload.attribution:
            attribution = payload.attribution
            db.add(
                AppointmentAttribution(
                    appointment_id=appointment.id,
                    marketing_session_id=attribution.marketing_session_id,
                    first_touch=(
                        attribution.first_touch.model_dump(mode="json", exclude_none=True)
                        if attribution.first_touch else None
                    ),
                    last_touch=(
                        attribution.last_touch.model_dump(mode="json", exclude_none=True)
                        if attribution.last_touch else None
                    ),
                    partner_code=attribution.partner_code,
                    traveler_segment=attribution.traveler_segment,
                    attribution_version=attribution.attribution_version,
                )
            )

        db.commit()
        db.refresh(appointment)
    except Exception as exc:
        db.rollback()
        error_msg = str(exc).lower()
        if "exclusion" in error_msg or "conflict" in error_msg or "no_double_booking" in error_msg:
            raise HTTPException(status_code=409, detail="Slot is no longer available")
        logger.error("Unexpected error creating appointment: %s", str(exc)[:200])
        raise HTTPException(status_code=500, detail="Could not create appointment")

    if appointment.source != "ci":
        try:
            send_appointment_emails(appointment, service.name)
        except Exception:
            logger.warning("Appointment %s created but email delivery failed", appointment.id)
    else:
        logger.info("Skipping email for CI smoke-test appointment %s", appointment.id)

    return _appointment_response(appointment, service)


@router.post("/internal/cleanup-ci", status_code=200)
def cleanup_ci(
    authorization: str | None = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
):
    """Delete CI smoke-test appointments older than 1 hour."""
    expected_token = f"Bearer {settings.cleanup_token}"

    if not authorization or authorization != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")

    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=1)

    deleted = (
        db.query(Appointment)
        .filter(
            Appointment.source == "ci",
            Appointment.created_at < cutoff,
        )
        .delete(synchronize_session="fetch")
    )
    db.commit()

    logger.info("CI cleanup: deleted %d old CI appointments", deleted)
    return {"deleted": deleted}


def _appointment_response(appointment: Appointment, service: Service) -> dict:
    """Build a response dict with derived service fields."""
    return {
        "id": appointment.id,
        "service_code": service.code,
        "service_name": service.name,
        "starts_at": appointment.starts_at,
        "ends_at": appointment.ends_at,
        "timezone": appointment.timezone,
        "first_name": appointment.first_name,
        "last_name": appointment.last_name,
        "status": appointment.status,
        "created_at": appointment.created_at,
    }
