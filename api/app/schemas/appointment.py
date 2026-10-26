"""Appointment schemas — creation and response.

The client sends service_code and starts_at. The server derives ends_at
from the service duration. ends_at from the client is ignored.

No clinical free text. No internal notes. Attribution fields are restricted
to non-clinical marketing metadata used for source-to-outcome measurement.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AttributionTouch(BaseModel):
    """One first-party acquisition touch, intentionally excluding PII/PHI."""

    source: str | None = Field(default=None, max_length=64)
    source_detail: str | None = Field(default=None, max_length=128)
    utm_source: str | None = Field(default=None, max_length=128)
    utm_medium: str | None = Field(default=None, max_length=128)
    utm_campaign: str | None = Field(default=None, max_length=256)
    utm_content: str | None = Field(default=None, max_length=256)
    utm_term: str | None = Field(default=None, max_length=256)
    gclid: str | None = Field(default=None, max_length=256)
    gbraid: str | None = Field(default=None, max_length=256)
    wbraid: str | None = Field(default=None, max_length=256)
    captured_at: datetime | None = None


class AppointmentAttributionIn(BaseModel):
    """Structured first-party attribution attached to one appointment."""

    marketing_session_id: str | None = Field(default=None, max_length=64)
    first_touch: AttributionTouch | None = None
    last_touch: AttributionTouch | None = None
    partner_code: str | None = Field(default=None, max_length=128)
    traveler_segment: Literal["yes", "no", "unknown"] = "unknown"
    attribution_version: str = Field(default="v1", max_length=16)


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
        max_length=32,
        examples=[None],
        description=(
            "Backward-compatible compact non-clinical source marker. Structured "
            "attribution belongs in attribution and must never contain medical information."
        ),
    )
    attribution: AppointmentAttributionIn | None = Field(
        default=None,
        description=(
            "Non-clinical first-party acquisition metadata only. Never include names, "
            "email, phone, symptoms, diagnosis, medications, reason-for-visit text, "
            "or other medical-record content."
        ),
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
