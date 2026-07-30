"""Admin API endpoints — Keycloak-protected.

GET  /api/v1/admin/me  — return the authenticated user's token claims.

More CRUD endpoints will be added in a follow-up step.
"""

import logging

from fastapi import APIRouter, Depends

from app.core.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter(tags=["admin"])


@router.get("/admin/me")
async def admin_me(user: dict = Depends(get_current_user)):
    """Return the authenticated user's identity and realm roles.

    Protected by Keycloak JWT — any valid token from the realm is accepted.
    Role-based authorization will be applied on real CRUD endpoints.
    """
    return {
        "sub": user["sub"],
        "preferred_username": user["preferred_username"],
        "email": user["email"],
        "roles": user["roles"],
    }
