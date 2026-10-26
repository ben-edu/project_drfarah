"""First-party marketing attribution linked to a scheduled appointment.

This table intentionally stores only non-clinical acquisition metadata.
Patient identity and clinical context remain on the appointment/clinical side;
marketing attribution is joined through appointment_id when business outcomes
such as ``visit_completed`` are evaluated.
"""

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class AppointmentAttribution(Base):
    __tablename__ = "appointment_attributions"
    __table_args__ = (
        UniqueConstraint("appointment_id", name="uq_appointment_attributions_appointment_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    appointment_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("appointments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    marketing_session_id: Mapped[str | None] = mapped_column(
        String(64), nullable=True, index=True
    )
    first_touch: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    last_touch: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    partner_code: Mapped[str | None] = mapped_column(String(128), nullable=True)
    traveler_segment: Mapped[str] = mapped_column(
        String(16), nullable=False, default="unknown", server_default="unknown"
    )
    attribution_version: Mapped[str] = mapped_column(
        String(16), nullable=False, default="v1", server_default="v1"
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
