"""Schemas for online patient registration.

The first phase intentionally excludes medical history, insurance identifiers,
documents, SSN, and clinical free text.
"""

from datetime import date, datetime

from pydantic import BaseModel, Field


NAME_PATTERN = r"^[a-zA-ZÀ-ÿ\-' ]*$"
PHONE_PATTERN = r"^[0-9+\-() .]*$"


class RegistrationData(BaseModel):
    appointment_reference: str | None = Field(default=None, max_length=64)
    first_name: str | None = Field(default=None, max_length=128, pattern=NAME_PATTERN)
    last_name: str | None = Field(default=None, max_length=128, pattern=NAME_PATTERN)
    date_of_birth: date | None = None
    email: str | None = Field(default=None, max_length=255, pattern=r"^$|^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$")
    phone: str | None = Field(default=None, max_length=64, pattern=PHONE_PATTERN)
    address_line1: str | None = Field(default=None, max_length=255)
    address_line2: str | None = Field(default=None, max_length=255)
    city: str | None = Field(default=None, max_length=128)
    state: str | None = Field(default=None, max_length=64)
    postal_code: str | None = Field(default=None, max_length=32)
    emergency_contact_name: str | None = Field(default=None, max_length=255)
    emergency_contact_phone: str | None = Field(default=None, max_length=64, pattern=PHONE_PATTERN)
    privacy_acknowledged: bool = False


class RegistrationCreate(RegistrationData):
    """A new saved draft must contain enough information to identify the patient."""

    first_name: str = Field(..., min_length=1, max_length=128, pattern=r"^[a-zA-ZÀ-ÿ\\-' ]+$")
    last_name: str = Field(..., min_length=1, max_length=128, pattern=r"^[a-zA-ZÀ-ÿ\\-' ]+$")
    email: str = Field(
        ...,
        max_length=255,
        pattern=r"^[a-zA-Z0-9._%+\\-]+@[a-zA-Z0-9.\\-]+\\.[a-zA-Z]{2,}$",
    )
    phone: str = Field(..., min_length=7, max_length=64, pattern=r"^[0-9+\\-() .]+$")


class RegistrationUpdate(RegistrationData):
    pass


class RegistrationResponse(RegistrationData):
    public_reference: str
    status: str
    updated_at: datetime
    submitted_at: datetime | None = None


class RegistrationCreatedResponse(RegistrationResponse):
    resume_token: str


class RegistrationSubmitResponse(BaseModel):
    public_reference: str
    status: str
    submitted_at: datetime
