"""Health check endpoints — used by Kubernetes liveness and readiness probes."""

import os

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.core.config import get_settings
from app.core.database import check_database_connection

router = APIRouter(tags=["health"])

settings = get_settings()


def _base_response(status: str) -> dict:
    return {
        "status": status,
        "service": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


def _configured_runtime_credential_readable() -> bool:
    """Return whether an explicitly configured ADC credential can be read.

    Local/dev/test environments do not need Google credentials unless
    ``GOOGLE_APPLICATION_CREDENTIALS`` is explicitly configured. In deployed
    environments the variable is set by the Kubernetes manifest, so an absent
    or unreadable file must fail readiness instead of allowing a silently broken
    offline-conversion integration.
    """

    credential_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if not credential_path:
        return True
    return os.path.isfile(credential_path) and os.access(credential_path, os.R_OK)


@router.get("/live")
def live() -> dict:
    """Liveness probe — confirmed the process is alive."""
    return _base_response("ok")


@router.get("/ready", response_model=None)
def ready(request: Request) -> dict | JSONResponse:
    """Readiness probe — confirms required runtime dependencies.

    Returns 200 when the database is reachable (or optional in dev/test) and
    any explicitly configured Google ADC credential file is readable.
    Returns 503 when a required runtime dependency is unavailable.
    """
    if settings.effective_database_url is None:
        # No database URL configured — in dev/test this is acceptable.
        if settings.ENVIRONMENT not in ("dev", "test"):
            # In staging/production, a missing database URL is a failure.
            return JSONResponse(
                status_code=503,
                content={"status": "not ready", "reason": "database not configured"},
            )
    elif not check_database_connection():
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "reason": "database unreachable"},
        )

    if not _configured_runtime_credential_readable():
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "reason": "runtime dependency unavailable"},
        )

    return _base_response("ok")
