"""Tests for booking endpoints.

Run from the api/ directory:
    PYTHONPATH=. python -m pytest -q tests/

Each test receives an isolated temporary SQLite database via tmp_path.
No state leaks between tests — test execution order does not matter.
"""

import os

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def setup_env(tmp_path: pytest.TempPathFactory):
    """Isolated environment — each test gets a unique temporary database."""
    db_path = tmp_path / "test.db"
    saved = {}
    for k in ("DATABASE_URL", "ENVIRONMENT", "SMTP_HOST", "SMTP_TEST_MODE"):
        saved[k] = os.environ.get(k)
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["ENVIRONMENT"] = "test"
    os.environ["SMTP_HOST"] = ""
    os.environ["SMTP_TEST_MODE"] = "true"

    from app.core.config import get_settings
    from app.core.database import reset_engine

    get_settings.cache_clear()
    reset_engine()

    import importlib
    import app.routers.health
    import app.main

    importlib.reload(app.routers.health)
    importlib.reload(app.main)

    yield app.main.app

    # Cleanup
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v
    get_settings.cache_clear()
    reset_engine()


VALID_BOOKING = {
    "service_type": "Urgent or acute care",
    "visit_type": "Clinic visit",
    "preferred_day": "Monday, July 27",
    "preferred_time": "10:00 AM",
    "time_window": "Late morning",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "+1-310-555-0189",
    "reason_category": "General appointment request",
}


def _client(app):
    return TestClient(app)


class TestBookingCreate:
    def test_creates_booking_returns_201(self, setup_env):
        app = setup_env
        with _client(app) as client:
            resp = client.post("/api/v1/bookings", json=VALID_BOOKING)
            assert resp.status_code == 201, resp.text

    def test_response_contains_booking_fields(self, setup_env):
        app = setup_env
        with _client(app) as client:
            resp = client.post("/api/v1/bookings", json=VALID_BOOKING)
            body = resp.json()
            assert isinstance(body["id"], int)
            assert body["id"] >= 1
            assert body["status"] == "requested"
            assert body["first_name"] == "Jane"
            assert body["last_name"] == "Doe"
            assert body["service_type"] == "Urgent or acute care"
            assert "created_at" in body

    def test_persistence_across_requests(self, setup_env):
        app = setup_env
        with _client(app) as client:
            r1 = client.post("/api/v1/bookings", json=VALID_BOOKING)
            assert r1.status_code == 201
            r2 = client.post("/api/v1/bookings", json=VALID_BOOKING)
            assert r2.status_code == 201
            # IDs must increase within the same isolated database.
            assert r2.json()["id"] > r1.json()["id"]

    def test_id_increments(self, setup_env):
        app = setup_env
        with _client(app) as client:
            r1 = client.post("/api/v1/bookings", json=VALID_BOOKING)
            r2 = client.post("/api/v1/bookings", json=VALID_BOOKING)
            r3 = client.post("/api/v1/bookings", json=VALID_BOOKING)
            id1 = r1.json()["id"]
            id2 = r2.json()["id"]
            id3 = r3.json()["id"]
            assert id2 == id1 + 1
            assert id3 == id2 + 1

    def test_no_secrets_in_response(self, setup_env):
        app = setup_env
        with _client(app) as client:
            resp = client.post("/api/v1/bookings", json=VALID_BOOKING)
            text = resp.text.lower()
            for forbidden in (
                "password", "token", "secret", "smtp",
                "psycopg", "postgresql", "database_url",
            ):
                assert forbidden not in text, f"'{forbidden}' found in response"


class TestBookingValidation:
    def test_rejects_missing_service_type(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING, "service_type": ""}
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 422

    def test_rejects_missing_first_name(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING, "first_name": ""}
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 422

    def test_rejects_invalid_email(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING, "email": "not-an-email"}
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 422

    def test_rejects_numeric_first_name(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING, "first_name": "Jane123"}
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 422

    def test_rejects_empty_payload(self, setup_env):
        app = setup_env
        with _client(app) as client:
            resp = client.post("/api/v1/bookings", json={})
            assert resp.status_code == 422

    def test_accepts_optional_time_window_missing(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING}
            del payload["time_window"]
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 201

    def test_accepts_accented_names(self, setup_env):
        app = setup_env
        with _client(app) as client:
            payload = {**VALID_BOOKING, "first_name": "José", "last_name": "Muñoz"}
            resp = client.post("/api/v1/bookings", json=payload)
            assert resp.status_code == 201
