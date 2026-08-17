"""Validation tests for the non-clinical appointment attribution source field."""

import pytest
from pydantic import ValidationError

from app.schemas.appointment import AppointmentCreate


BASE_PAYLOAD = {
    "service_code": "urgent-care",
    "starts_at": "2026-08-18T10:00:00-07:00",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "+1-310-555-0189",
    "reason_category": "General appointment request",
}


def test_source_accepts_database_column_limit():
    marker = "x" * 32
    model = AppointmentCreate(**BASE_PAYLOAD, source=marker)
    assert model.source == marker


def test_source_rejects_value_longer_than_database_column():
    with pytest.raises(ValidationError):
        AppointmentCreate(**BASE_PAYLOAD, source="x" * 33)
