"""Booking model — minimal persistence for appointment requests.

Fields are deliberately limited. No clinical free text is stored.
PHI is restricted to name, email, and phone as required for scheduling.
"""

import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Booking(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    service_type: Mapped[str] = mapped_column(String(128), nullable=False)
    visit_type: Mapped[str] = mapped_column(String(128), nullable=False)
    preferred_day: Mapped[str] = mapped_column(String(64), nullable=False)
    preferred_time: Mapped[str] = mapped_column(String(32), nullable=False)
    time_window: Mapped[str | None] = mapped_column(String(64), nullable=True)
    first_name: Mapped[str] = mapped_column(String(128), nullable=False)
    last_name: Mapped[str] = mapped_column(String(128), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str] = mapped_column(String(64), nullable=False)
    reason_category: Mapped[str] = mapped_column(String(128), nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="requested", nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
