"""Tests for the admin auth layer — no live Keycloak required.

Generates RSA keypairs and mints RS256 JWTs to exercise every code path in
app.core.auth without external dependencies.
"""

import json
import time
from unittest import mock

import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# Test keypair and JWKS helpers
# ---------------------------------------------------------------------------

def _generate_rsa_keypair():
    """Return (private_key, public_key) — both are cryptography key objects."""
    private = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public = private.public_key()
    return private, public


def _public_jwk(public_key, kid="test-kid-001"):
    """Build a JWK dict from a public key (RS256 compatible)."""
    from jwt.algorithms import RSAAlgorithm

    jwk_str = RSAAlgorithm.to_jwk(public_key)
    jwk = json.loads(jwk_str) if isinstance(jwk_str, str) else jwk_str
    jwk["kid"] = kid
    jwk["use"] = "sig"
    jwk["alg"] = "RS256"
    return jwk


def _jwks_response(jwk):
    """Return a full JWKS dict as Keycloak would."""
    return {"keys": [jwk]}


def _mint_token(
    private_key,
    *,
    issuer="https://keycloak.soria-academie.fr/realms/drfarah",
    audience=None,
    sub="test-user-123",
    preferred_username="dr.farah",
    email="farah@example.com",
    roles=None,
    kid="test-kid-001",
    exp=None,
    nbf=None,
    iat=None,
):
    """Mint a valid RS256 JWT with the given claims."""
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": sub,
        "preferred_username": preferred_username,
        "email": email,
        "realm_access": {"roles": roles or []},
        "iat": iat or now,
        "nbf": nbf or now,
        "exp": exp or (now + 3600),
    }
    if audience:
        payload["aud"] = audience

    headers = {"kid": kid}
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


# ---------------------------------------------------------------------------
# Auth dependency tests (unit-level, no HTTP)
# ---------------------------------------------------------------------------

class TestDecodeAndVerify:
    """Unit tests for _decode_and_verify — the core verification logic."""

    def test_valid_token_returns_payload(self, monkeypatch):
        private, public = _generate_rsa_keypair()
        jwks = _jwks_response(_public_jwk(public))
        monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)

        token = _mint_token(private, roles=["clinic-admin"])
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings

        settings = Settings(ENVIRONMENT="test")
        payload = _decode_and_verify(token, settings)

        assert payload["sub"] == "test-user-123"
        assert payload["preferred_username"] == "dr.farah"
        assert payload["realm_access"]["roles"] == ["clinic-admin"]

    def test_missing_token_raises(self):
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings

        settings = Settings(ENVIRONMENT="test")
        with pytest.raises(Exception):
            _decode_and_verify("not.a.real.token", settings)

    def test_wrong_issuer_raises_401(self, monkeypatch):
        private, public = _generate_rsa_keypair()
        jwks = _jwks_response(_public_jwk(public))
        monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)

        token = _mint_token(private, issuer="https://evil.example.com/realms/fake")
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings
        from fastapi import HTTPException

        settings = Settings(ENVIRONMENT="test")
        with pytest.raises(HTTPException) as exc_info:
            _decode_and_verify(token, settings)
        assert exc_info.value.status_code == 401
        assert "issuer" in exc_info.value.detail.lower()

    def test_expired_token_raises_401(self, monkeypatch):
        private, public = _generate_rsa_keypair()
        jwks = _jwks_response(_public_jwk(public))
        monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)

        now = int(time.time())
        token = _mint_token(
            private, exp=now - 10, nbf=now - 20, iat=now - 20
        )
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings
        from fastapi import HTTPException

        settings = Settings(ENVIRONMENT="test")
        with pytest.raises(HTTPException) as exc_info:
            _decode_and_verify(token, settings)
        assert exc_info.value.status_code == 401
        assert "expired" in exc_info.value.detail.lower()

    def test_wrong_signing_key_raises_401(self, monkeypatch):
        """Token signed with a DIFFERENT key than what's in the JWKS."""
        _, public = _generate_rsa_keypair()
        jwks = _jwks_response(_public_jwk(public))
        monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)

        # Sign with a different key
        other_private, _ = _generate_rsa_keypair()
        token = _mint_token(other_private, roles=["clinic-admin"])
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings
        from fastapi import HTTPException

        settings = Settings(ENVIRONMENT="test")
        with pytest.raises(HTTPException) as exc_info:
            _decode_and_verify(token, settings)
        assert exc_info.value.status_code == 401

    def test_unknown_kid_refreshes_and_retries(self, monkeypatch):
        """When the token's kid is not in the initial JWKS, we refetch."""
        private, public = _generate_rsa_keypair()
        jwk = _public_jwk(public, kid="rotated-kid")
        jwks = _jwks_response(jwk)

        # First call returns a JWKS with a different kid
        call_count = [0]

        def _mock_fetch(settings):
            call_count[0] += 1
            if call_count[0] == 1:
                # First call: return a JWKS WITHOUT the matching kid
                dummy_key = _public_jwk(public, kid="old-kid")
                return {"keys": [dummy_key]}
            # Second call: return the real JWKS
            return jwks

        monkeypatch.setattr("app.core.auth._fetch_jwks", _mock_fetch)

        token = _mint_token(private, kid="rotated-kid", roles=["clinic-staff"])
        from app.core.auth import _decode_and_verify
        from app.core.config import Settings

        settings = Settings(ENVIRONMENT="test")
        payload = _decode_and_verify(token, settings)
        assert payload["sub"] == "test-user-123"
        assert call_count[0] == 2  # refetched


class TestRequireRealmRole:
    """Unit tests for the require_realm_role dependency factory."""

    @pytest.mark.anyio
    async def test_role_present_passes(self):
        from app.core.auth import require_realm_role

        dep = require_realm_role("clinic-admin")
        user = {"sub": "u1", "roles": ["clinic-admin", "clinic-staff"]}
        result = await dep(user)
        assert result == user

    @pytest.mark.anyio
    async def test_role_missing_raises_403(self):
        from app.core.auth import require_realm_role
        from fastapi import HTTPException

        dep = require_realm_role("clinic-admin")
        user = {"sub": "u1", "roles": ["clinic-staff"]}
        with pytest.raises(HTTPException) as exc_info:
            await dep(user)
        assert exc_info.value.status_code == 403


# ---------------------------------------------------------------------------
# Integration tests (via TestClient)
# ---------------------------------------------------------------------------

@pytest.fixture
def auth_app(monkeypatch):
    """Return a TestClient wired to a fresh app, with JWKS mocked."""
    import os

    os.environ.setdefault("ENVIRONMENT", "test")
    os.environ.setdefault("SMTP_TEST_MODE", "true")

    from app.core.config import get_settings

    get_settings.cache_clear()
    from app.core.database import reset_engine

    reset_engine()

    # Generate a keypair and inject the JWKS
    private, public = _generate_rsa_keypair()
    jwk = _public_jwk(public, kid="integration-test-kid")
    jwks = _jwks_response(jwk)

    # Patch _fetch_jwks AND _force_refresh_jwks so all paths use our JWKS
    monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)
    monkeypatch.setattr("app.core.auth._force_refresh_jwks", lambda s: jwks)

    # Force a fresh import so the patches take effect
    import app.main
    import app.routers.admin
    import importlib

    importlib.reload(app.routers.admin)
    importlib.reload(app.main)

    client = TestClient(app.main.app)
    client._test_private_key = private
    return client


class TestAdminMeEndpoint:
    """Integration tests for GET /api/v1/admin/me."""

    def test_valid_token_returns_200(self, auth_app):
        token = _mint_token(
            auth_app._test_private_key,
            roles=["clinic-admin"],
            kid="integration-test-kid",
        )
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["sub"] == "test-user-123"
        assert body["preferred_username"] == "dr.farah"
        assert "clinic-admin" in body["roles"]

    def test_no_token_returns_401(self, auth_app):
        resp = auth_app.get("/api/v1/admin/me")
        assert resp.status_code == 401

    def test_wrong_key_returns_401(self, auth_app):
        """Token signed by a different key than the one in the JWKS."""
        other_private, _ = _generate_rsa_keypair()
        token = _mint_token(
            other_private, roles=["clinic-admin"], kid="integration-test-kid"
        )
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401

    def test_expired_token_returns_401(self, auth_app):
        now = int(time.time())
        token = _mint_token(
            auth_app._test_private_key,
            roles=["clinic-admin"],
            kid="integration-test-kid",
            exp=now - 10,
            nbf=now - 20,
            iat=now - 20,
        )
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401

    def test_wrong_issuer_returns_401(self, auth_app):
        token = _mint_token(
            auth_app._test_private_key,
            issuer="https://fake.example.com/realms/evil",
            roles=["clinic-admin"],
            kid="integration-test-kid",
        )
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 401

    def test_token_without_roles_works(self, auth_app):
        """A valid token without any realm roles should still pass get_current_user."""
        token = _mint_token(
            auth_app._test_private_key,
            roles=[],
            kid="integration-test-kid",
        )
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert resp.status_code == 200
        assert resp.json()["roles"] == []

    def test_invalid_header_returns_401(self, auth_app):
        resp = auth_app.get(
            "/api/v1/admin/me",
            headers={"Authorization": "Bearer not.a.jwt"},
        )
        assert resp.status_code == 401
