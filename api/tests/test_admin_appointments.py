"""Tests for admin appointment endpoints — Keycloak auth + CRUD.

Uses the same RSA-keypair / JWKS monkeypatch approach as test_admin_auth.py.
Each test gets an isolated SQLite database via the conftest.py db_session fixture.
"""

import datetime
import json
import time
from urllib.parse import quote

import jwt
import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient


# ---------------------------------------------------------------------------
# RSA keypair + JWT helpers (same approach as test_admin_auth.py)
# ---------------------------------------------------------------------------


def _generate_rsa_keypair():
    private = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public = private.public_key()
    return private, public


def _public_jwk(public_key, kid="admin-test-kid"):
    from jwt.algorithms import RSAAlgorithm

    jwk_str = RSAAlgorithm.to_jwk(public_key)
    jwk = json.loads(jwk_str) if isinstance(jwk_str, str) else jwk_str
    jwk["kid"] = kid
    jwk["use"] = "sig"
    jwk["alg"] = "RS256"
    return jwk


def _jwks_response(jwk):
    return {"keys": [jwk]}


def _mint_token(
    private_key,
    *,
    issuer="https://keycloak.soria-academie.fr/realms/drfarah",
    sub="test-user-123",
    preferred_username="dr.farah",
    email="farah@example.com",
    roles=None,
    kid="admin-test-kid",
    exp=None,
):
    now = int(time.time())
    payload = {
        "iss": issuer,
        "sub": sub,
        "preferred_username": preferred_username,
        "email": email,
        "realm_access": {"roles": roles or []},
        "iat": now,
        "nbf": now,
        "exp": exp or (now + 3600),
    }
    headers = {"kid": kid}
    return jwt.encode(payload, private_key, algorithm="RS256", headers=headers)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def admin_client(db_session, seed_services, monkeypatch):
    """TestClient with mocked Keycloak auth + seeded services + isolated DB.

    Depends on the autouse db_session (conftest.py) which provides an
    isolated SQLite database with all tables created.  seed_services
    inserts the standard service catalog so appointment FKs resolve.
    """
    private, public = _generate_rsa_keypair()
    jwk = _public_jwk(public, kid="admin-test-kid")
    jwks = _jwks_response(jwk)

    monkeypatch.setattr("app.core.auth._fetch_jwks", lambda s: jwks)
    monkeypatch.setattr("app.core.auth._force_refresh_jwks", lambda s: jwks)

    import app.routers.admin
    import app.main
    import importlib

    importlib.reload(app.routers.admin)
    importlib.reload(app.main)

    client = TestClient(app.main.app)
    client._test_private_key = private
    client._test_db = db_session
    return client


def _auth_headers(client, roles=None):
    """Return Authorization headers with a valid JWT for the given roles."""
    token = _mint_token(client._test_private_key, roles=roles or [])
    return {"Authorization": f"Bearer {token}"}


def _seed_appointment(db, **overrides):
    """Insert one appointment and return it.

    Default values produce a valid pending appointment for urgent-care.
    """
    from app.models.appointment import Appointment
    from app.models.service import Service

    svc = db.query(Service).filter(Service.code == "urgent-care").first()
    now = datetime.datetime.now(datetime.timezone.utc)

    defaults = {
        "service_id": svc.id,
        "starts_at": now + datetime.timedelta(days=7),
        "ends_at": now + datetime.timedelta(days=7, minutes=30),
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane@example.com",
        "phone": "+1-310-555-0189",
        "reason_category": "General",
        "status": "pending",
    }
    defaults.update(overrides)

    appt = Appointment(**defaults)
    db.add(appt)
    db.commit()
    db.refresh(appt)
    return appt


# ---------------------------------------------------------------------------
# Auth tests — 401 / 403 gates
# ---------------------------------------------------------------------------


class TestAuthRequired:
    def test_list_no_token_returns_401(self, admin_client):
        resp = admin_client.get("/api/v1/admin/appointments")
        assert resp.status_code == 401

    def test_detail_no_token_returns_401(self, admin_client):
        resp = admin_client.get("/api/v1/admin/appointments/1")
        assert resp.status_code == 401

    def test_patch_no_token_returns_401(self, admin_client):
        resp = admin_client.patch(
            "/api/v1/admin/appointments/1",
            json={"status": "confirmed"},
        )
        assert resp.status_code == 401

    def test_list_no_roles_returns_403(self, admin_client):
        headers = _auth_headers(admin_client, roles=[])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        assert resp.status_code == 403

    def test_detail_no_roles_returns_403(self, admin_client):
        headers = _auth_headers(admin_client, roles=[])
        resp = admin_client.get("/api/v1/admin/appointments/1", headers=headers)
        assert resp.status_code == 403

    def test_patch_no_roles_returns_403(self, admin_client):
        headers = _auth_headers(admin_client, roles=[])
        resp = admin_client.patch(
            "/api/v1/admin/appointments/1",
            json={"status": "confirmed"},
            headers=headers,
        )
        assert resp.status_code == 403

    def test_staff_role_passes(self, admin_client):
        """clinic-staff → 200 on list."""
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        assert resp.status_code == 200

    def test_admin_role_inherits_staff(self, admin_client):
        """clinic-admin inherits clinic-staff via Keycloak composite role."""
        headers = _auth_headers(admin_client, roles=["clinic-admin", "clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        assert resp.status_code == 200


# ---------------------------------------------------------------------------
# GET /admin/appointments — list with filters & pagination
# ---------------------------------------------------------------------------


class TestListAppointments:
    def test_empty_list(self, admin_client):
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["items"] == []
        assert body["total"] == 0
        assert body["limit"] == 25
        assert body["offset"] == 0

    def test_returns_seeded_appointments(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, first_name="Alice", email="alice@example.com")
        _seed_appointment(db, first_name="Bob", email="bob@example.com")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        assert len(body["items"]) == 2
        assert body["items"][0]["first_name"] in ("Alice", "Bob")

    def test_fields_present(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, first_name="Carol", email="carol@example.com")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        item = resp.json()["items"][0]
        for field in (
            "id", "service_code", "service_name", "starts_at",
            "first_name", "last_name", "email", "phone",
            "reason_category", "status", "source", "created_at",
        ):
            assert field in item, f"Missing field: {field}"

    def test_service_name_resolved(self, admin_client):
        """service_name must come from the Service relationship, not be None."""
        db = admin_client._test_db
        _seed_appointment(db)

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        item = resp.json()["items"][0]
        assert item["service_code"] == "urgent-care"
        assert item["service_name"] == "Urgent or acute care"

    def test_pagination_limit_offset(self, admin_client):
        db = admin_client._test_db
        for i in range(5):
            _seed_appointment(db, email=f"user{i}@example.com")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        # Page 1: limit=2, offset=0
        resp = admin_client.get(
            "/api/v1/admin/appointments?limit=2&offset=0", headers=headers
        )
        body = resp.json()
        assert body["total"] == 5
        assert len(body["items"]) == 2
        assert body["limit"] == 2
        assert body["offset"] == 0

        # Page 2: limit=2, offset=2
        resp = admin_client.get(
            "/api/v1/admin/appointments?limit=2&offset=2", headers=headers
        )
        body = resp.json()
        assert body["total"] == 5
        assert len(body["items"]) == 2
        assert body["offset"] == 2

        # Page 3: limit=2, offset=4 (only 1 item left)
        resp = admin_client.get(
            "/api/v1/admin/appointments?limit=2&offset=4", headers=headers
        )
        body = resp.json()
        assert len(body["items"]) == 1

    def test_status_filter(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, first_name="Pending1", status="pending")
        _seed_appointment(db, first_name="Confirmed1", status="confirmed")
        _seed_appointment(db, first_name="Confirmed2", status="confirmed")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments?status=confirmed", headers=headers
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["total"] == 2
        names = [i["first_name"] for i in body["items"]]
        assert all("Confirmed" in n for n in names)

    def test_invalid_status_returns_422(self, admin_client):
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments?status=invalid_status", headers=headers
        )
        assert resp.status_code == 422

    def test_q_filter_name(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, first_name="Alice")
        _seed_appointment(db, first_name="Bob")
        _seed_appointment(db, first_name="Alicia")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments?q=Ali", headers=headers)
        body = resp.json()
        assert body["total"] == 2

    def test_q_filter_email(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, email="unique@example.com")
        _seed_appointment(db, email="other@example.com")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments?q=unique@example", headers=headers
        )
        body = resp.json()
        assert body["total"] == 1

    def test_q_filter_phone(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db, phone="+1-310-555-9999")
        _seed_appointment(db, phone="+1-212-555-0000")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments?q=310-555", headers=headers
        )
        body = resp.json()
        assert body["total"] == 1

    def test_q_filter_by_id(self, admin_client):
        db = admin_client._test_db
        appt = _seed_appointment(
            db, first_name="Target", phone="+9-999-999-9999"
        )
        _seed_appointment(
            db, first_name="Other", phone="+8-888-888-8888"
        )

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            f"/api/v1/admin/appointments?q={appt.id}", headers=headers
        )
        body = resp.json()
        assert body["total"] == 1
        assert body["items"][0]["id"] == appt.id

    def test_date_from_filter(self, admin_client):
        db = admin_client._test_db
        base = datetime.datetime.now(datetime.timezone.utc)
        _seed_appointment(
            db,
            first_name="Future",
            starts_at=base + datetime.timedelta(days=30),
        )
        _seed_appointment(
            db,
            first_name="NearFuture",
            starts_at=base + datetime.timedelta(days=3),
        )

        cutoff = (base + datetime.timedelta(days=14)).isoformat()
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            f"/api/v1/admin/appointments?date_from={quote(cutoff)}",
            headers=headers,
        )
        body = resp.json()
        assert body["total"] == 1
        assert body["items"][0]["first_name"] == "Future"

    def test_date_to_filter(self, admin_client):
        db = admin_client._test_db
        base = datetime.datetime.now(datetime.timezone.utc)
        _seed_appointment(
            db,
            first_name="Past",
            starts_at=base + datetime.timedelta(days=2),
        )
        _seed_appointment(
            db,
            first_name="Later",
            starts_at=base + datetime.timedelta(days=60),
        )

        cutoff = (base + datetime.timedelta(days=30)).isoformat()
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            f"/api/v1/admin/appointments?date_to={quote(cutoff)}",
            headers=headers,
        )
        body = resp.json()
        assert body["total"] == 1
        assert body["items"][0]["first_name"] == "Past"

    def test_order_desc(self, admin_client):
        db = admin_client._test_db
        base = datetime.datetime.now(datetime.timezone.utc)
        _seed_appointment(
            db,
            first_name="Earlier",
            starts_at=base + datetime.timedelta(days=5),
        )
        _seed_appointment(
            db,
            first_name="Later",
            starts_at=base + datetime.timedelta(days=10),
        )

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments?order=starts_at.desc", headers=headers
        )
        body = resp.json()
        assert body["items"][0]["first_name"] == "Later"
        assert body["items"][1]["first_name"] == "Earlier"

    def test_no_sensitive_fields_in_response(self, admin_client):
        db = admin_client._test_db
        _seed_appointment(db)

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get("/api/v1/admin/appointments", headers=headers)
        text = resp.text.lower()
        for forbidden in (
            "password", "token", "secret", "smtp",
            "psycopg", "database_url", "stack", "traceback",
        ):
            assert forbidden not in text, f"'{forbidden}' found in response"


# ---------------------------------------------------------------------------
# GET /admin/appointments/{id} — detail
# ---------------------------------------------------------------------------


class TestGetAppointment:
    def test_existing_returns_200(self, admin_client):
        db = admin_client._test_db
        appt = _seed_appointment(db, first_name="DetailTest")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            f"/api/v1/admin/appointments/{appt.id}", headers=headers
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["id"] == appt.id
        assert body["first_name"] == "DetailTest"
        assert body["service_code"] == "urgent-care"
        assert body["service_name"] == "Urgent or acute care"
        for field in ("ends_at", "timezone", "updated_at"):
            assert field in body, f"Missing field: {field}"

    def test_missing_returns_404(self, admin_client):
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.get(
            "/api/v1/admin/appointments/99999", headers=headers
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# PATCH /admin/appointments/{id} — status update
# ---------------------------------------------------------------------------


class TestPatchAppointment:
    def test_valid_status_transition(self, admin_client):
        db = admin_client._test_db
        appt = _seed_appointment(db, status="pending")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.patch(
            f"/api/v1/admin/appointments/{appt.id}",
            json={"status": "confirmed"},
            headers=headers,
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["status"] == "confirmed"
        assert body["id"] == appt.id

        # Verify it was persisted (expire all to bust the identity map,
        # since the PATCH endpoint uses a different session).
        from app.models.appointment import Appointment

        db.expire_all()
        updated = db.query(Appointment).filter(Appointment.id == appt.id).first()
        assert updated.status == "confirmed"

    def test_all_valid_statuses(self, admin_client):
        """Every documented status value should be accepted."""
        db = admin_client._test_db

        valid_statuses = ["pending", "confirmed", "cancelled", "completed", "no_show"]
        for target in valid_statuses:
            appt = _seed_appointment(db, status="pending")
            headers = _auth_headers(admin_client, roles=["clinic-staff"])
            resp = admin_client.patch(
                f"/api/v1/admin/appointments/{appt.id}",
                json={"status": target},
                headers=headers,
            )
            assert resp.status_code == 200, f"Failed to transition to {target}: {resp.text}"
            assert resp.json()["status"] == target

    def test_invalid_status_returns_422(self, admin_client):
        db = admin_client._test_db
        appt = _seed_appointment(db, status="pending")

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.patch(
            f"/api/v1/admin/appointments/{appt.id}",
            json={"status": "unknown_status"},
            headers=headers,
        )
        assert resp.status_code == 422

    def test_missing_id_returns_404(self, admin_client):
        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.patch(
            "/api/v1/admin/appointments/99999",
            json={"status": "confirmed"},
            headers=headers,
        )
        assert resp.status_code == 404

    def test_patch_also_requires_role(self, admin_client):
        """PATCH with a valid token but no clinic-staff role → 403."""
        db = admin_client._test_db
        appt = _seed_appointment(db, status="pending")

        headers = _auth_headers(admin_client, roles=[])
        resp = admin_client.patch(
            f"/api/v1/admin/appointments/{appt.id}",
            json={"status": "confirmed"},
            headers=headers,
        )
        assert resp.status_code == 403

    def test_no_emails_sent_on_status_change(self, admin_client, monkeypatch):
        """Admin status changes must NOT trigger patient emails."""
        db = admin_client._test_db
        appt = _seed_appointment(db, status="pending")

        # Guard: if anything tries to call send_appointment_emails, fail.
        called = []

        def _fake_send(*args, **kwargs):
            called.append(True)

        monkeypatch.setattr(
            "app.emails.appointment.send_appointment_emails", _fake_send
        )

        headers = _auth_headers(admin_client, roles=["clinic-staff"])
        resp = admin_client.patch(
            f"/api/v1/admin/appointments/{appt.id}",
            json={"status": "confirmed"},
            headers=headers,
        )
        assert resp.status_code == 200
        assert len(called) == 0, (
            "send_appointment_emails was called — admin PATCH must NOT send emails"
        )
