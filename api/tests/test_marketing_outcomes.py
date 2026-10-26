"""Tests for the privacy-safe marketing outcome read model."""

import datetime

from app.models.appointment import Appointment
from app.models.appointment_attribution import AppointmentAttribution
from app.models.service import Service
from app.services.marketing_outcomes import build_visit_completed_rows


def _appointment(db, *, status: str, source: str | None = None) -> Appointment:
    service = db.query(Service).filter(Service.code == "urgent-care").first()
    starts_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=2)
    appointment = Appointment(
        service_id=service.id,
        starts_at=starts_at,
        ends_at=starts_at + datetime.timedelta(minutes=30),
        first_name="Private",
        last_name="Patient",
        email="private@example.com",
        phone="+1-310-555-0199",
        reason_category="General appointment request",
        status=status,
        source=source,
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment


def test_only_completed_appointments_generate_outcomes(db_session, seed_services):
    completed = _appointment(db_session, status="completed", source="google_ads")
    _appointment(db_session, status="confirmed", source="google_ads")
    _appointment(db_session, status="cancelled", source="google_ads")

    rows = build_visit_completed_rows(db_session)

    assert len(rows) == 1
    assert rows[0]["outcome_key"] == f"visit_completed:{completed.id}"
    assert rows[0]["event_name"] == "visit_completed"
    assert rows[0]["source"] == "google_ads"
    assert rows[0]["occurred_at"] == completed.starts_at


def test_attribution_prefers_last_touch_and_preserves_click_ids(db_session, seed_services):
    completed = _appointment(db_session, status="completed", source="direct")
    attribution = AppointmentAttribution(
        appointment_id=completed.id,
        marketing_session_id="mkt-session-123",
        first_touch={"source": "google_organic"},
        last_touch={
            "source": "google_ads",
            "gclid": "test-gclid",
            "gbraid": "test-gbraid",
            "wbraid": "test-wbraid",
        },
        partner_code="hotel-001",
        traveler_segment="yes",
        attribution_version="v1",
    )
    db_session.add(attribution)
    db_session.commit()

    row = build_visit_completed_rows(db_session)[0]

    assert row["source"] == "google_ads"
    assert row["gclid"] == "test-gclid"
    assert row["gbraid"] == "test-gbraid"
    assert row["wbraid"] == "test-wbraid"
    assert row["marketing_session_id"] == "mkt-session-123"
    assert row["partner_code"] == "hotel-001"
    assert row["traveler_segment"] == "yes"


def test_outcome_contract_excludes_patient_and_clinical_fields(db_session, seed_services):
    _appointment(db_session, status="completed", source="google_organic")

    row = build_visit_completed_rows(db_session)[0]

    forbidden = {
        "first_name",
        "last_name",
        "email",
        "phone",
        "reason_category",
        "service_id",
        "service_code",
        "service_name",
    }
    assert forbidden.isdisjoint(row.keys())


def test_completed_without_attribution_remains_reportable(db_session, seed_services):
    completed = _appointment(db_session, status="completed", source=None)

    row = build_visit_completed_rows(db_session)[0]

    assert row["outcome_key"] == f"visit_completed:{completed.id}"
    assert row["source"] == "unknown"
    assert row["gclid"] is None
    assert row["marketing_session_id"] is None
    assert row["traveler_segment"] == "unknown"
