"""Appointment scheduling endpoints.

GET  /api/v1/services            — list active services
GET  /api/v1/availability        — available appointment slots
POST /api/v1/appointments        — create a scheduled appointment
POST /api/v1/internal/cleanup-ci — clean up CI smoke-test records (token-protected)
"""

import datetime
import logging

from fastapi import APIRouter, Depends, Header, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.database import get_db
from app.models.appointment import Appointment
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

# ------------------------------------------------------------------
# POST /api/v1/bookings is preserved as a legacy endpoint in
# app/routers/booking.py. It stores free-text day/time preferences
# without real scheduling. New integrations should use this router.
# ------------------------------------------------------------------


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
    """Return available appointment slots for a service and date range.

    Dates must be ISO 8601 (YYYY-MM-DD). Maximum range is 31 days.
    Only future slots within working hours are returned. Blocked periods
    and existing appointments are excluded.
    """
    # Validate service.
    service = (
        db.query(Service)
        .filter(Service.code == service_code, Service.is_active == True)
        .first()
    )
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    # Validate dates.
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

    # Generate slots.
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


@router.post("/appointments", response_model=AppointmentResponse, status_code=201)
def create_appointment(
    payload: AppointmentCreate,
    db: Session = Depends(get_db),
):
    """Create a scheduled appointment.

    The server derives ends_at from the selected service duration and
    buffers. The starts_at is the appointment start time (client-provided).
    Concurrent requests for the same slot receive HTTP 409.
    """
    # Validate service.
    service = (
        db.query(Service)
        .filter(Service.code == payload.service_code, Service.is_active == True)
        .first()
    )
    if service is None:
        raise HTTPException(status_code=404, detail="Service not found")

    # Parse and validate starts_at.
    try:
        starts_at = datetime.datetime.fromisoformat(payload.starts_at)
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid starts_at format — use ISO 8601")

    # Ensure starts_at is UTC-aware.
    if starts_at.tzinfo is None:
        raise HTTPException(
            status_code=422, detail="starts_at must include a timezone offset"
        )
    starts_at_utc = starts_at.astimezone(datetime.timezone.utc)

    # Reject past slots.
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    if starts_at_utc <= now_utc:
        raise HTTPException(status_code=422, detail="Slot is in the past")

    # Validate slot is within working hours.
    if not scheduling.validate_slot_in_working_hours(db, starts_at_utc, service):
        raise HTTPException(status_code=422, detail="Slot is outside working hours")

    # Check blocked periods.
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

    # Check for appointment conflicts (application-level, before DB constraint).
    if scheduling.check_slot_conflict(db, service, starts_at_utc):
        raise HTTPException(status_code=409, detail="Slot is no longer available")

    # Derive ends_at.
    ends_at_utc = starts_at_utc + duration

    # Create appointment.
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
        source=None,
    )

    try:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)
    except Exception as exc:
        db.rollback()
        # Check if this is a PostgreSQL exclusion-constraint violation.
        error_msg = str(exc).lower()
        if "exclusion" in error_msg or "conflict" in error_msg or "no_double_booking" in error_msg:
            raise HTTPException(status_code=409, detail="Slot is no longer available")
        logger.error("Unexpected error creating appointment: %s", str(exc)[:200])
        raise HTTPException(status_code=500, detail="Could not create appointment")

    return _appointment_response(appointment, service)


@router.post("/internal/cleanup-ci", status_code=200)
def cleanup_ci(
    authorization: str | None = Header(None, alias="Authorization"),
    db: Session = Depends(get_db),
):
    """Delete CI smoke-test appointments older than 1 hour.

    Requires a pre-shared token: Authorization: Bearer <token>.
    Only deletes records where source='ci'. Not a public endpoint.
    """
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
