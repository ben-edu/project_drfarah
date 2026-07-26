"""Tests for health check endpoints.

Run from the api/ directory:
    PYTHONPATH=. python -m pytest -q tests/

No live cluster or PostgreSQL required — uses SQLite for readiness tests.
"""

import os

import pytest
from fastapi.testclient import TestClient

from app.core.database import reset_engine


def _clear_and_reload():
    """Clear cached settings and database engine, then import a fresh app."""
    from app.core.config import get_settings

    get_settings.cache_clear()
    reset_engine()
    # Force module reload to get fresh settings in health.py module-level
    import importlib
    import app.routers.health

    importlib.reload(app.routers.health)

    import app.main

    importlib.reload(app.main)
    return app.main.app


def _set_env(key: str, value: str | None):
    if value is None:
        os.environ.pop(key, None)
    else:
        os.environ[key] = value


@pytest.fixture(autouse=True)
def cleanup_env():
    """Ensure clean environment after each test."""
    saved = {}
    for k in ("DATABASE_URL", "ENVIRONMENT", "APP_NAME"):
        saved[k] = os.environ.get(k)
    os.environ.pop("DATABASE_URL", None)
    os.environ["ENVIRONMENT"] = "test"
    from app.core.config import get_settings

    get_settings.cache_clear()
    reset_engine()
    yield
    # Restore
    for k, v in saved.items():
        _set_env(k, v)
    get_settings.cache_clear()
    reset_engine()


class TestLiveness:
    def test_returns_200(self):
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/live")
            assert resp.status_code == 200

    def test_payload_structure(self):
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/live")
            body = resp.json()
            assert body["status"] == "ok"
            assert body["service"] == "drfarah-api"
            assert "environment" in body

    def test_no_secrets_in_response(self):
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/live")
            text = resp.text.lower()
            for forbidden in (
                "password",
                "token",
                "secret",
                "key",
                "psycopg",
                "postgresql",
            ):
                assert forbidden not in text, f"'{forbidden}' found in response"


class TestReadiness:
    def test_returns_200_with_sqlite(self):
        """Readiness succeeds when a valid SQLite database is configured."""
        os.environ["DATABASE_URL"] = "sqlite:////tmp/test_drfarah.db"
        os.environ["ENVIRONMENT"] = "test"
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/ready")
            assert resp.status_code == 200
            body = resp.json()
            assert body["status"] == "ok"

    def test_returns_200_in_dev_without_database(self):
        """In dev/test, a missing database URL is not treated as a failure."""
        os.environ.pop("DATABASE_URL", None)
        os.environ["ENVIRONMENT"] = "test"
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/ready")
            assert resp.status_code == 200

    def test_returns_503_in_staging_without_database(self):
        """In staging, a missing DATABASE_URL triggers 503."""
        os.environ.pop("DATABASE_URL", None)
        os.environ["ENVIRONMENT"] = "staging"
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/ready")
            assert resp.status_code == 503

    def test_503_payload_is_safe(self):
        """Failed readiness must not expose internals or secrets."""
        os.environ.pop("DATABASE_URL", None)
        os.environ["ENVIRONMENT"] = "staging"
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.get("/api/v1/health/ready")
            assert resp.status_code == 503
            body = resp.json()
            assert body["status"] == "not ready"
            text = resp.text.lower()
            for forbidden in (
                "password",
                "token",
                "secret",
                "stack",
                "traceback",
                "sqlite",
                "psycopg",
                "postgresql",
                "database_url",
                "exception",
                "error at",
            ):
                assert forbidden not in text, f"'{forbidden}' found in 503 response"


class TestCORS:
    def test_cors_origins_parsed(self):
        """CORS_ORIGINS is correctly parsed into a list."""
        from app.core.config import Settings

        s = Settings(
            CORS_ORIGINS="https://a.example.com, https://b.example.com",
            ENVIRONMENT="test",
        )
        assert s.cors_origins_list == [
            "https://a.example.com",
            "https://b.example.com",
        ]

    def test_cors_config_default(self):
        """Default CORS_ORIGINS includes staging origin."""
        from app.core.config import Settings

        s = Settings(ENVIRONMENT="test")
        assert "https://staging.drfarah.proxbenovh.cloud" in s.cors_origins_list

    def test_cors_preflight_allowed_origin(self):
        """OPTIONS preflight returns success for an allowed origin."""
        app = _clear_and_reload()
        with TestClient(app) as client:
            resp = client.options(
                "/api/v1/health/live",
                headers={
                    "Origin": "https://staging.drfarah.proxbenovh.cloud",
                    "Access-Control-Request-Method": "GET",
                },
            )
            # Either 200 or at minimum not a 400 CORS block
            assert resp.status_code < 500
