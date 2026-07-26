"""Booking request endpoint — create and acknowledge appointment requests.

POST /api/v1/bookings  —  create a new booking request.
"""

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.booking import Booking
from app.schemas.booking import BookingCreate, BookingResponse
from app.services.email import send_booking_notification

logger = logging.getLogger(__name__)
router = APIRouter(tags=["booking"])


@router.post("/bookings", response_model=BookingResponse, status_code=201)
def create_booking(payload: BookingCreate, db: Session = Depends(get_db)):
    """Create a new booking request.

    The booking is persisted and a notification email is triggered.
    No clinical free text is accepted.
    """
    booking = Booking(
        service_type=payload.service_type,
        visit_type=payload.visit_type,
        preferred_day=payload.preferred_day,
        preferred_time=payload.preferred_time,
        time_window=payload.time_window,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=payload.email,
        phone=payload.phone,
        reason_category=payload.reason_category,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # Trigger notification (fire-and-forget — failure does not block response).
    send_booking_notification({
        "first_name": booking.first_name,
        "last_name": booking.last_name,
        "service_type": booking.service_type,
        "visit_type": booking.visit_type,
        "preferred_day": booking.preferred_day,
        "preferred_time": booking.preferred_time,
        "time_window": booking.time_window,
        "reason_category": booking.reason_category,
        "email": booking.email,
        "phone": booking.phone,
    })

    return booking
