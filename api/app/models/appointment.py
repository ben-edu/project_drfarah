"""Appointment model — scheduled patient appointments.

Stores confirmed time slots with UTC timestamps. The service_id FK
links to the selected service.

Double-booking is prevented by a PostgreSQL exclusion constraint on
(starts_at, ends_at) for non-cancelled appointments. Application-level
checks provide an additional safety layer.

Status values:
  pending   — created through public booking, awaiting clinic confirmation
  confirmed — clinic has accepted the appointment
  cancelled — patient or clinic cancelled
  completed — patient was seen
  no_show   — patient did not arrive
"""

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("services.id", ondelete="RESTRICT"), nullable=False
    )
    starts_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, index=True
    )
    ends_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    timezone: Mapped[str] = mapped_column(
        String(64), nullable=False, default="America/Los_Angeles",
        server_default="America/Los_Angeles",
    )
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_category: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(
        String(32), nullable=False, default="pending", server_default="pending",
        index=True,
    )
    source: Mapped[str | None] = mapped_column(String(32), nullable=True, default=None)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    service: Mapped["Service"] = relationship("Service")  # noqa: F821
