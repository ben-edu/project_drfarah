"""Patient registration model.

Stores patient demographic/contact registration separately from appointment booking.
No medical-history free text, insurance identifiers, uploaded documents, or clinical
notes are collected in this first registration phase.
"""

import datetime

from sqlalchemy import Boolean, Date, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class PatientRegistration(Base):
    __tablename__ = "patient_registrations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    public_reference: Mapped[str] = mapped_column(String(32), unique=True, nullable=False, index=True)
    resume_token_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    status: Mapped[str] = mapped_column(String(24), nullable=False, default="draft", server_default="draft", index=True)

    appointment_reference: Mapped[str | None] = mapped_column(String(64), nullable=True)

    first_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(128), nullable=True)
    date_of_birth: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(64), nullable=True)

    address_line1: Mapped[str | None] = mapped_column(String(255), nullable=True)
    address_line2: Mapped[str | None] = mapped_column(String(255), nullable=True)
    city: Mapped[str | None] = mapped_column(String(128), nullable=True)
    state: Mapped[str | None] = mapped_column(String(64), nullable=True)
    postal_code: Mapped[str | None] = mapped_column(String(32), nullable=True)

    emergency_contact_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    emergency_contact_phone: Mapped[str | None] = mapped_column(String(64), nullable=True)

    privacy_acknowledged: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    submitted_at: Mapped[datetime.datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
