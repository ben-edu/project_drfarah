"""Booking request and response schemas — safe validation only.

No clinical free text. No excessive PHI. No insurance or ID numbers.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class BookingCreate(BaseModel):
    """Incoming booking request from the frontend."""

    service_type: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=["Urgent or acute care"],
    )
    visit_type: str = Field(
        ...,
        min_length=1,
        max_length=128,
        examples=["Clinic visit"],
    )
    preferred_day: str = Field(
        ...,
        min_length=1,
        max_length=64,
        examples=["Monday, July 27"],
    )
    preferred_time: str = Field(
        ...,
        min_length=1,
        max_length=32,
        examples=["10:00 AM"],
    )
    time_window: Optional[str] = Field(
        default=None,
        max_length=64,
        examples=["Late morning"],
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


class BookingResponse(BaseModel):
    """Returned to the frontend after a successful booking request."""

    id: int
    service_type: str
    visit_type: str
    preferred_day: str
    preferred_time: str
    time_window: Optional[str] = None
    first_name: str
    last_name: str
    reason_category: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
