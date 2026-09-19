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


class AdminRegistrationListItem(BaseModel):
    """One row in the admin patient-registration list."""

    id: int
    public_reference: str
    appointment_reference: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    status: str
    updated_at: datetime
    submitted_at: datetime | None = None


class AdminRegistrationDetail(AdminRegistrationListItem):
    """Full registration detail — never includes the resume-token hash."""

    date_of_birth: str | None = None
    address_line1: str | None = None
    address_line2: str | None = None
    city: str | None = None
    state: str | None = None
    postal_code: str | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    privacy_acknowledged: bool


class PaginatedRegistrationResponse(BaseModel):
    items: list[AdminRegistrationListItem]
    total: int
    limit: int
    offset: int


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
