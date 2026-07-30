"""Admin API endpoints — Keycloak-protected.

GET  /api/v1/admin/me                          — return the authenticated user's token claims.
GET  /api/v1/admin/appointments                — list appointments (clinic-staff+)
GET  /api/v1/admin/appointments/{appointment_id} — appointment detail (clinic-staff+)
PATCH /api/v1/admin/appointments/{appointment_id} — update appointment status (clinic-staff+)
"""

import datetime
import logging
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_ as sa_or_
from sqlalchemy.orm import Session, joinedload

from app.core.auth import get_current_user, require_realm_role
from app.core.database import get_db
from app.models.appointment import Appointment
from app.schemas.admin import (
    AdminAppointmentDetail,
    AdminAppointmentListItem,
    AppointmentStatusEnum,
    AppointmentStatusUpdate,
    PaginatedAppointmentResponse,
)

logger = logging.getLogger(__name__)
router = APIRouter(tags=["admin"])

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _admin_appointment_list_item(appt: Appointment) -> dict:
    """Build a dict for AdminAppointmentListItem from an ORM object.

    The caller must ensure that appt.service is eagerly loaded (joinedload
    or selectinload) to avoid N+1 queries.
    """
    return {
        "id": appt.id,
        "service_code": appt.service.code,
        "service_name": appt.service.name,
        "starts_at": appt.starts_at,
        "first_name": appt.first_name,
        "last_name": appt.last_name,
        "email": appt.email,
        "phone": appt.phone,
        "reason_category": appt.reason_category,
        "status": appt.status,
        "source": appt.source,
        "created_at": appt.created_at,
    }


def _admin_appointment_detail(appt: Appointment) -> dict:
    """Build a dict for AdminAppointmentDetail from an ORM object."""
    return {
        "id": appt.id,
        "service_code": appt.service.code,
        "service_name": appt.service.name,
        "starts_at": appt.starts_at,
        "ends_at": appt.ends_at,
        "timezone": appt.timezone,
        "first_name": appt.first_name,
        "last_name": appt.last_name,
        "email": appt.email,
        "phone": appt.phone,
        "reason_category": appt.reason_category,
        "status": appt.status,
        "source": appt.source,
        "created_at": appt.created_at,
        "updated_at": appt.updated_at,
    }


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.get("/admin/me")
async def admin_me(user: dict = Depends(get_current_user)):
    """Return the authenticated user's identity and realm roles.

    Protected by Keycloak JWT — any valid token from the realm is accepted.
    """
    return {
        "sub": user["sub"],
        "preferred_username": user["preferred_username"],
        "email": user["email"],
        "roles": user["roles"],
    }


@router.get(
    "/admin/appointments",
    response_model=PaginatedAppointmentResponse,
    dependencies=[Depends(require_realm_role("clinic-staff"))],
)
def list_admin_appointments(
    status_filter: Optional[str] = Query(
        default=None,
        alias="status",
        description="Filter by appointment status (e.g. pending, confirmed)",
    ),
    date_from: Optional[str] = Query(
        default=None,
        description="ISO date/datetime — filter starts_at >= this value",
    ),
    date_to: Optional[str] = Query(
        default=None,
        description="ISO date/datetime — filter starts_at <= this value",
    ),
    q: Optional[str] = Query(
        default=None,
        description="Search query — matches name, email, phone, or appointment id",
    ),
    limit: int = Query(default=25, ge=1, le=100, description="Page size"),
    offset: int = Query(default=0, ge=0, description="Offset for pagination"),
    order: str = Query(
        default="starts_at.asc",
        description="Sort field and direction: starts_at.asc (default) or starts_at.desc",
    ),
    db: Session = Depends(get_db),
):
    """List appointments with filtering and pagination.

    Requires clinic-staff (or clinic-admin, which inherits it).
    """
    # --- Build base query (eager-load service to avoid N+1) ---
    query = db.query(Appointment).options(joinedload(Appointment.service))

    # --- Status filter ---
    if status_filter is not None:
        if status_filter not in AppointmentStatusEnum.__members__:
            raise HTTPException(
                status_code=422,
                detail=f"Invalid status '{status_filter}'. "
                f"Valid values: {', '.join(AppointmentStatusEnum.__members__)}",
            )
        query = query.filter(Appointment.status == status_filter)

    # --- Date range filters ---
    if date_from is not None:
        try:
            dt_from = datetime.datetime.fromisoformat(date_from)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid date_from format — use ISO 8601 (e.g. 2026-07-01 or 2026-07-01T00:00:00)",
            )
        query = query.filter(Appointment.starts_at >= dt_from)

    if date_to is not None:
        try:
            dt_to = datetime.datetime.fromisoformat(date_to)
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid date_to format — use ISO 8601 (e.g. 2026-07-31 or 2026-07-31T23:59:59)",
            )
        query = query.filter(Appointment.starts_at <= dt_to)

    # --- Free-text search ---
    if q is not None:
        search = f"%{q}%"
        # Also match by integer id if q looks like a number.
        filters = [
            Appointment.first_name.ilike(search),
            Appointment.last_name.ilike(search),
            Appointment.email.ilike(search),
            Appointment.phone.ilike(search),
        ]
        try:
            ref_id = int(q)
            filters.append(Appointment.id == ref_id)
        except ValueError:
            pass
        query = query.filter(sa_or_(*filters))

    # --- Count total (before pagination) ---
    total = query.count()

    # --- Ordering ---
    if order == "starts_at.desc":
        query = query.order_by(Appointment.starts_at.desc())
    else:
        query = query.order_by(Appointment.starts_at.asc())

    # --- Pagination ---
    appointments = query.offset(offset).limit(limit).all()

    items = [_admin_appointment_list_item(a) for a in appointments]
    return {
        "items": items,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get(
    "/admin/appointments/{appointment_id}",
    response_model=AdminAppointmentDetail,
    dependencies=[Depends(require_realm_role("clinic-staff"))],
)
def get_admin_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Return full detail for a single appointment.

    Requires clinic-staff (or clinic-admin, which inherits it).
    """
    appt = (
        db.query(Appointment)
        .options(joinedload(Appointment.service))
        .filter(Appointment.id == appointment_id)
        .first()
    )
    if appt is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return _admin_appointment_detail(appt)


@router.patch(
    "/admin/appointments/{appointment_id}",
    response_model=AdminAppointmentDetail,
    dependencies=[Depends(require_realm_role("clinic-staff"))],
)
def patch_admin_appointment(
    appointment_id: int,
    body: AppointmentStatusUpdate,
    db: Session = Depends(get_db),
):
    """Update an appointment's status.

    Requires clinic-staff (or clinic-admin, which inherits it).
    Does NOT send patient notification emails in this step.
    """
    appt = (
        db.query(Appointment)
        .options(joinedload(Appointment.service))
        .filter(Appointment.id == appointment_id)
        .first()
    )
    if appt is None:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appt.status = body.status.value
    appt.updated_at = datetime.datetime.now(datetime.timezone.utc)
    db.commit()
    db.refresh(appt)

    logger.info(
        "Admin status update: appointment %s -> %s by staff",
        appointment_id,
        body.status.value,
    )

    return _admin_appointment_detail(appt)

