"""Appointment schemas — creation and response.

The client sends service_code and starts_at. The server derives ends_at
from the service duration. ends_at from the client is ignored.

No clinical free text. No internal notes. No sensitive fields.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class AppointmentCreate(BaseModel):
    """Incoming appointment request from the public booking form."""

    service_code: str = Field(
        ...,
        min_length=1,
        max_length=64,
        examples=["urgent-care"],
    )
    starts_at: str = Field(
        ...,
        examples=["2026-07-28T09:00:00-07:00"],
        description="ISO 8601 timestamp with offset",
    )
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        pattern=r"^[a-zA-ZÀ-ÿ\-' ]+$",
        examples=["Jane"],
    )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=128,
        pattern=r"^[a-zA-ZÀ-ÿ\-' ]+$",
        examples=["Doe"],
    )
    email: str = Field(
        ...,
        max_length=255,
        pattern=r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$",
        examples=["jane@example.com"],
    )
    phone: str = Field(
        ...,
        min_length=7,
        max_length=64,
        pattern=r"^[0-9+\-() .]+$",
        examples=["+1-310-555-0189"],
    )
    reason_category: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=["General appointment request"],
    )
    source: str | None = Field(
        default=None,
        max_length=64,
        examples=[None],
        description="Internal marker (e.g. 'ci' for CI smoke tests). Not exposed to patients.",
    )


class AppointmentResponse(BaseModel):
    """Returned to the client after successful appointment creation."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    service_code: str
    service_name: str
    starts_at: datetime
    ends_at: datetime
    timezone: str
    first_name: str
    last_name: str
    status: str
    created_at: datetime
