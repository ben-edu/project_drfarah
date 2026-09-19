"""Tests for online patient registration draft/resume/submit flow."""

import importlib

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine


@pytest.fixture(autouse=True)
def test_app_setup():
    import app.main
    importlib.reload(app.main)
    yield app.main.app
    reset_engine()


def _client(app):
    return TestClient(app)


DRAFT = {
    "appointment_reference": "WEB-TEST",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane@example.com",
    "phone": "+1-310-555-0189",
}


class TestPatientRegistration:
    def test_create_returns_private_resume_token(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            r = client.post("/api/v1/patient-registrations", json=DRAFT)
            assert r.status_code == 201, r.text
            body = r.json()
            assert body["public_reference"].startswith("REG-")
            assert body["status"] == "draft"
            assert len(body["resume_token"]) > 20

    def test_resume_requires_token(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            created = client.post("/api/v1/patient-registrations", json=DRAFT).json()
            ref = created["public_reference"]
            r = client.get(f"/api/v1/patient-registrations/{ref}")
            assert r.status_code == 401

    def test_save_and_resume(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            created = client.post("/api/v1/patient-registrations", json=DRAFT).json()
            ref = created["public_reference"]
            token = created["resume_token"]
            headers = {"X-Registration-Token": token}
            update = {
                **DRAFT,
                "date_of_birth": "1990-01-02",
                "address_line1": "100 Test Street",
                "city": "Beverly Hills",
                "state": "CA",
                "postal_code": "90210",
                "privacy_acknowledged": True,
            }
            r = client.patch(f"/api/v1/patient-registrations/{ref}", json=update, headers=headers)
            assert r.status_code == 200, r.text
            r2 = client.get(f"/api/v1/patient-registrations/{ref}", headers=headers)
            assert r2.status_code == 200
            assert r2.json()["city"] == "Beverly Hills"

    def test_submit_rejects_incomplete(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            created = client.post("/api/v1/patient-registrations", json=DRAFT).json()
            ref = created["public_reference"]
            headers = {"X-Registration-Token": created["resume_token"]}
            r = client.post(f"/api/v1/patient-registrations/{ref}/submit", headers=headers)
            assert r.status_code == 422

    def test_submit_complete_registration(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            created = client.post("/api/v1/patient-registrations", json=DRAFT).json()
            ref = created["public_reference"]
            headers = {"X-Registration-Token": created["resume_token"]}
            update = {
                **DRAFT,
                "date_of_birth": "1990-01-02",
                "address_line1": "100 Test Street",
                "city": "Beverly Hills",
                "state": "CA",
                "postal_code": "90210",
                "privacy_acknowledged": True,
            }
            assert client.patch(f"/api/v1/patient-registrations/{ref}", json=update, headers=headers).status_code == 200
            r = client.post(f"/api/v1/patient-registrations/{ref}/submit", headers=headers)
            assert r.status_code == 200, r.text
            assert r.json()["status"] == "submitted"

    def test_submitted_registration_is_read_only(self, db_session, test_app_setup):
        with _client(test_app_setup) as client:
            created = client.post("/api/v1/patient-registrations", json=DRAFT).json()
            ref = created["public_reference"]
            headers = {"X-Registration-Token": created["resume_token"]}
            update = {
                **DRAFT,
                "date_of_birth": "1990-01-02",
                "address_line1": "100 Test Street",
                "city": "Beverly Hills",
                "state": "CA",
                "postal_code": "90210",
                "privacy_acknowledged": True,
            }
            client.patch(f"/api/v1/patient-registrations/{ref}", json=update, headers=headers)
            client.post(f"/api/v1/patient-registrations/{ref}/submit", headers=headers)
            r = client.patch(f"/api/v1/patient-registrations/{ref}", json={**update, "city": "Los Angeles"}, headers=headers)
            assert r.status_code == 409
