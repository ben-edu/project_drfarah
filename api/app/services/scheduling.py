"""Scheduling service — availability generation and conflict detection.

All times are stored in UTC. Clinic timezone is America/Los_Angeles.
Slot increment: 15 minutes.
"""

import datetime
import logging
from zoneinfo import ZoneInfo

from sqlalchemy.orm import Session

from app.models.appointment import Appointment
from app.models.blocked_period import BlockedPeriod
from app.models.service import Service
from app.models.working_hours import WorkingHours

logger = logging.getLogger(__name__)

CLINIC_TIMEZONE = ZoneInfo("America/Los_Angeles")
SLOT_INCREMENT_MINUTES = 15
MAX_AVAILABILITY_DAYS = 31


def _utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)


def _to_utc(dt: datetime.datetime, tz: ZoneInfo) -> datetime.datetime:
    """Convert a timezone-aware datetime to UTC, or localize a naive one."""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=tz)
    return dt.astimezone(datetime.timezone.utc)


def _ensure_utc(dt: datetime.datetime) -> datetime.datetime:
    """Ensure a datetime is UTC-aware. Naive datetimes are assumed to be UTC.

    SQLite stores datetimes without timezone info, so values read back
    from the database may be naive even though the column was declared
    with timezone=True. This helper normalizes them for comparison.
    """
    if dt.tzinfo is None:
        return dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)


def generate_availability(
    db: Session,
    service: Service,
    start_date: datetime.date,
    end_date: datetime.date,
) -> list[dict]:
    """Generate available appointment slots for a service within a date range.

    Returns a list of {starts_at, ends_at} dicts with ISO 8601 timestamps.
    Slots are generated at 15-minute increments within working hours, with
    blocked periods and existing appointments removed.
    """
    now_utc = _utc_now()
    tz = CLINIC_TIMEZONE
    duration = datetime.timedelta(minutes=service.duration_minutes)
    buffer_before = datetime.timedelta(minutes=service.buffer_before_minutes)
    buffer_after = datetime.timedelta(minutes=service.buffer_after_minutes)
    increment = datetime.timedelta(minutes=SLOT_INCREMENT_MINUTES)

    # Load working-hour intervals active for the requested date range.
    working_hours_records = (
        db.query(WorkingHours)
        .filter(
            WorkingHours.is_active == True,
            WorkingHours.effective_from <= end_date,
        )
        .filter(
            (WorkingHours.effective_until.is_(None))
            | (WorkingHours.effective_until >= start_date)
        )
        .all()
    )

    # Group by weekday.
    wh_by_weekday: dict[int, list[tuple[datetime.time, datetime.time]]] = {}
    for wh in working_hours_records:
        wh_by_weekday.setdefault(wh.weekday, []).append(
            (wh.start_time, wh.end_time)
        )

    # Load blocked periods overlapping the date range.
    range_start_utc = _to_utc(
        datetime.datetime.combine(start_date, datetime.time.min, tzinfo=tz), tz
    )
    range_end_utc = _to_utc(
        datetime.datetime.combine(end_date, datetime.time.max, tzinfo=tz), tz
    )
    blocked_periods = (
        db.query(BlockedPeriod)
        .filter(
            BlockedPeriod.is_active == True,
            BlockedPeriod.starts_at < range_end_utc,
            BlockedPeriod.ends_at > range_start_utc,
        )
        .all()
    )

    # Load existing non-cancelled appointments in the range.
    existing_appointments = (
        db.query(Appointment)
        .filter(
            Appointment.status.notin_(["cancelled", "no_show"]),
            Appointment.starts_at < range_end_utc,
            Appointment.ends_at > range_start_utc,
        )
        .all()
    )

    slots = []
    current_date = start_date

    while current_date <= end_date:
        py_weekday = current_date.weekday()  # 0=Monday..6=Sunday
        day_intervals = wh_by_weekday.get(py_weekday, [])

        for wh_start_time, wh_end_time in day_intervals:
            # Build the working-hour interval for this day in clinic time.
            wh_start_dt = datetime.datetime.combine(
                current_date, wh_start_time, tzinfo=tz
            )
            wh_end_dt = datetime.datetime.combine(
                current_date, wh_end_time, tzinfo=tz
            )

            # The first valid slot start must allow buffer_before.
            slot_start = wh_start_dt + buffer_before

            while slot_start + duration <= wh_end_dt:
                slot_end = slot_start + duration

                # Occupied range includes buffers.
                occupied_start = slot_start - buffer_before
                occupied_end = slot_end + buffer_after

                # Skip if the slot is in the past.
                slot_start_utc = slot_start.astimezone(datetime.timezone.utc)
                if slot_start_utc <= now_utc:
                    slot_start += increment
                    continue

                # Check occupied range is within working hours.
                if occupied_start < wh_start_dt or occupied_end > wh_end_dt:
                    slot_start += increment
                    continue

                # Check against blocked periods.
                conflict = False
                occ_start_utc = occupied_start.astimezone(datetime.timezone.utc)
                occ_end_utc = occupied_end.astimezone(datetime.timezone.utc)
                for bp in blocked_periods:
                    if occ_start_utc < _ensure_utc(bp.ends_at) and occ_end_utc > _ensure_utc(bp.starts_at):
                        conflict = True
                        break
                if conflict:
                    slot_start += increment
                    continue

                # Check against existing appointments.
                for appt in existing_appointments:
                    if occ_start_utc < _ensure_utc(appt.ends_at) and occ_end_utc > _ensure_utc(appt.starts_at):
                        conflict = True
                        break
                if conflict:
                    slot_start += increment
                    continue

                slots.append({
                    "starts_at": slot_start_utc.isoformat(),
                    "ends_at": slot_end.astimezone(datetime.timezone.utc).isoformat(),
                })

                slot_start += increment

        current_date += datetime.timedelta(days=1)

    return slots


def check_slot_conflict(
    db: Session,
    service: Service,
    slot_start_utc: datetime.datetime,
    exclude_appointment_id: int | None = None,
) -> bool:
    """Return True if the requested slot conflicts with an existing appointment.

    Checks the occupied range (slot + buffers) against non-cancelled
    appointments. Does not check working hours or blocked periods
    (those are validated separately).
    """
    tz = CLINIC_TIMEZONE
    duration = datetime.timedelta(minutes=service.duration_minutes)
    buffer_before = datetime.timedelta(minutes=service.buffer_before_minutes)
    buffer_after = datetime.timedelta(minutes=service.buffer_after_minutes)

    occ_start = slot_start_utc - buffer_before
    occ_end = slot_start_utc + duration + buffer_after

    query = db.query(Appointment).filter(
        Appointment.status.notin_(["cancelled", "no_show"]),
        Appointment.starts_at < occ_end,
        Appointment.ends_at > occ_start,
    )

    if exclude_appointment_id is not None:
        query = query.filter(Appointment.id != exclude_appointment_id)

    return db.query(query.exists()).scalar()


def validate_slot_in_working_hours(
    db: Session,
    slot_start_utc: datetime.datetime,
    service: Service,
) -> bool:
    """Return True if the slot falls entirely within active working hours.

    The occupied range (slot + buffers) must fit within at least one
    working-hour interval on the slot's day in the clinic timezone.
    """
    tz = CLINIC_TIMEZONE
    slot_dt = slot_start_utc.astimezone(tz)
    slot_date = slot_dt.date()
    slot_time = slot_dt.time()
    py_weekday = slot_date.weekday()

    duration = datetime.timedelta(minutes=service.duration_minutes)
    buffer_before = datetime.timedelta(minutes=service.buffer_before_minutes)
    buffer_after = datetime.timedelta(minutes=service.buffer_after_minutes)

    occ_start_time = (
        datetime.datetime.combine(datetime.date.min, slot_time)
        - buffer_before
    ).time()
    occ_end_dt = datetime.datetime.combine(datetime.date.min, slot_time) + duration + buffer_after
    occ_end_time = occ_end_dt.time()

    intervals = (
        db.query(WorkingHours)
        .filter(
            WorkingHours.is_active == True,
            WorkingHours.weekday == py_weekday,
            WorkingHours.effective_from <= slot_date,
        )
        .filter(
            (WorkingHours.effective_until.is_(None))
            | (WorkingHours.effective_until >= slot_date)
        )
        .all()
    )

    for wh in intervals:
        if occ_start_time >= wh.start_time and occ_end_time <= wh.end_time:
            return True

    return False
