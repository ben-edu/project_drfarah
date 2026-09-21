"""Tests for GET /api/v1/services — active service listing."""

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine


@pytest.fixture(autouse=True)
def test_app_setup():
    """Fresh app instance for each test."""
    import importlib
    import app.main
    importlib.reload(app.main)

    yield app.main.app

    reset_engine()


def _client(app):
    return TestClient(app)


class TestServicesEndpoint:
    def test_returns_200(self, db_session, seed_services, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            assert resp.status_code == 200

    def test_returns_all_active_services(self, db_session, seed_services, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            body = resp.json()
            assert len(body["services"]) == 4

    def test_each_service_has_required_fields(self, db_session, seed_services, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            for svc in resp.json()["services"]:
                assert "code" in svc
                assert "name" in svc
                assert "duration_minutes" in svc
                assert isinstance(svc["duration_minutes"], int)

    def test_service_codes_are_unique(self, db_session, seed_services, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            codes = [s["code"] for s in resp.json()["services"]]
            assert len(codes) == len(set(codes))

    def test_inactive_service_not_returned(self, db_session, test_app_setup):
        from app.models.service import Service
        svc = Service(code="hidden", name="Hidden", duration_minutes=10,
                      is_active=False)
        db_session.add(svc)
        db_session.commit()

        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            codes = [s["code"] for s in resp.json()["services"]]
            assert "hidden" not in codes

    def test_empty_services_returns_empty_list(self, db_session, test_app_setup):
        """When no active services exist, return an empty list."""
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            body = resp.json()
            assert body["services"] == []

    def test_no_secrets_in_response(self, db_session, seed_services, test_app_setup):
        app = test_app_setup
        with _client(app) as client:
            resp = client.get("/api/v1/services")
            text = resp.text.lower()
            for forbidden in ("password", "token", "secret", "smtp", "database_url"):
                assert forbidden not in text, f"'{forbidden}' found in response"
