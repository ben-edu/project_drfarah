"""Service schemas — public service information.

Only active, non-sensitive fields are exposed.
"""

from pydantic import BaseModel, ConfigDict


class ServiceOut(BaseModel):
    """Public service representation."""
    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    description: str | None = None
    duration_minutes: int
    buffer_before_minutes: int
    buffer_after_minutes: int


class ServiceListResponse(BaseModel):
    services: list[ServiceOut]
