"""Keycloak JWT authentication for the admin API.

Provides FastAPI dependencies that verify RS256-signed JWTs against the
Keycloak realm's JWKS endpoint, with in-process caching.
"""

import logging
import time
from typing import Optional

import httpx
import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.config import get_settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# JWKS cache
# ---------------------------------------------------------------------------

_jwks: Optional[dict] = None
_jwks_fetched_at: float = 0.0
JWKS_TTL_SECONDS = 3600  # re-fetch hourly at most


def _fetch_jwks(settings) -> dict:
    """Fetch the JWKS from Keycloak, caching in-process.

    Re-fetches if the cache is empty, expired, or if the caller signals
    that a kid was unknown (force_refresh=True).
    """
    global _jwks, _jwks_fetched_at

    now = time.monotonic()
    if _jwks is not None and (now - _jwks_fetched_at) < JWKS_TTL_SECONDS:
        return _jwks

    try:
        resp = httpx.get(settings.KEYCLOAK_JWKS_URL, timeout=10.0)
        resp.raise_for_status()
        _jwks = resp.json()
        _jwks_fetched_at = now
        logger.debug("JWKS fetched from %s", settings.KEYCLOAK_JWKS_URL)
        return _jwks
    except Exception as exc:
        logger.error("Failed to fetch JWKS from %s: %s", settings.KEYCLOAK_JWKS_URL, exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify credentials (JWKS unavailable)",
        )


def _force_refresh_jwks(settings) -> dict:
    """Force a fresh JWKS fetch (used when an unknown kid is encountered)."""
    global _jwks, _jwks_fetched_at
    _jwks = None
    _jwks_fetched_at = 0.0
    return _fetch_jwks(settings)


# ---------------------------------------------------------------------------
# Token verification helpers
# ---------------------------------------------------------------------------

def _decode_and_verify(token: str, settings) -> dict:
    """Decode and verify a JWT, returning the claims dict.

    Raises HTTPException(401) on any verification failure.
    """
    jwks = _fetch_jwks(settings)

    # Decode the header (without verification) to get the kid.
    try:
        unverified_header = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token header",
        ) from exc

    kid = unverified_header.get("kid")
    if not kid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing key ID (kid)",
        )

    # Find the matching key in the JWKS.
    key_data = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key_data = k
            break

    if key_data is None:
        # Unknown kid — the key may have rotated. Force a refresh and retry.
        logger.debug("Unknown kid %s — refreshing JWKS", kid)
        jwks = _force_refresh_jwks(settings)
        for k in jwks.get("keys", []):
            if k.get("kid") == kid:
                key_data = k
                break

    if key_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unknown signing key",
        )

    # Build the public key from the JWKS entry.
    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(key_data)
    except Exception as exc:
        logger.error("Failed to construct public key from JWKS: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Unable to verify credentials",
        ) from exc

    # Verify the token.
    try:
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=settings.KEYCLOAK_ISSUER,
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_nbf": True,
                "verify_iss": True,
                "verify_aud": settings.KEYCLOAK_VERIFY_AUD,
            },
            audience=settings.KEYCLOAK_AUDIENCE if settings.KEYCLOAK_VERIFY_AUD else None,
        )
    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        ) from exc
    except jwt.InvalidIssuerError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token issuer",
        ) from exc
    except jwt.InvalidAudienceError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token audience",
        ) from exc
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc

    return payload


def _extract_user(payload: dict) -> dict:
    """Extract a small user dict from a verified token payload."""
    realm_access = payload.get("realm_access") or {}
    return {
        "sub": payload.get("sub", ""),
        "preferred_username": payload.get("preferred_username", ""),
        "email": payload.get("email", ""),
        "roles": realm_access.get("roles", []),
    }


# ---------------------------------------------------------------------------
# FastAPI dependencies
# ---------------------------------------------------------------------------

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> dict:
    """FastAPI dependency — verify the Bearer token and return the current user.

    Returns a dict with keys: sub, preferred_username, email, roles.
    Raises HTTP 401 if the token is missing, invalid, or expired.
    """
    settings = get_settings()

    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
        )

    token = credentials.credentials
    payload = _decode_and_verify(token, settings)
    user = _extract_user(payload)

    logger.debug(
        "Authenticated user: sub=%s username=%s roles=%s",
        user["sub"],
        user["preferred_username"],
        user["roles"],
    )
    return user


def require_realm_role(role: str):
    """Dependency factory — require a specific Keycloak realm role.

    Usage:
        @router.get("/admin/something")
        async def endpoint(user = Depends(require_realm_role("clinic-admin"))):
            ...
    """

    async def _dependency(user: dict = Depends(get_current_user)) -> dict:
        if role not in user["roles"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires realm role '{role}'",
            )
        return user

    return _dependency
