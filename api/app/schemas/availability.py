"""Availability schemas — available appointment slots."""

from pydantic import BaseModel


class SlotOut(BaseModel):
    starts_at: str
    ends_at: str


class AvailabilityServiceInfo(BaseModel):
    code: str
    name: str
    duration_minutes: int


class AvailabilityResponse(BaseModel):
    service: AvailabilityServiceInfo
    timezone: str
    slots: list[SlotOut]
