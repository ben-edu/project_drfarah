"""Admin API schemas — appointment management.

All admin endpoints require Keycloak authentication with the clinic-staff
realm role (or clinic-admin, which inherits clinic-staff).
"""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class AppointmentStatusEnum(str, Enum):
    """Valid appointment status values — matches the documented statuses.

    These are the ONLY values accepted by the PATCH status endpoint.
    """

    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"
    no_show = "no_show"


class AdminAppointmentListItem(BaseModel):
    """One row in the admin appointment list."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    service_code: str
    service_name: str
    starts_at: datetime
    first_name: str
    last_name: str
    email: str
    phone: str
    reason_category: str
    status: str
    source: str | None = None
    created_at: datetime


class AdminAppointmentDetail(BaseModel):
    """Full appointment detail (currently same shape as the list item)."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    service_code: str
    service_name: str
    starts_at: datetime
    ends_at: datetime
    timezone: str
    first_name: str
    last_name: str
    email: str
    phone: str
    reason_category: str
    status: str
    source: str | None = None
    created_at: datetime
    updated_at: datetime


class AppointmentStatusUpdate(BaseModel):
    """Request body for PATCH /admin/appointments/{id} — status transition."""

    status: AppointmentStatusEnum = Field(
        ..., description="New status — must be a valid appointment status value"
    )


class PaginatedAppointmentResponse(BaseModel):
    """Paginated envelope for admin appointment list."""

    items: list[AdminAppointmentListItem]
    total: int
    limit: int
    offset: int
