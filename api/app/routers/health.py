"""Health check endpoints — used by Kubernetes liveness and readiness probes."""

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


@router.get("/live")
def live() -> dict:
    """Liveness probe — confirmed the process is alive."""
    return _base_response("ok")


@router.get("/ready", response_model=None)
def ready(request: Request) -> dict | JSONResponse:
    """Readiness probe — confirms database connectivity.

    Returns 200 when the database is reachable.
    Returns 503 when the database is not reachable or not configured in
    a non-dev environment.
    """
    if settings.effective_database_url is None:
        # No database URL configured — in dev/test this is acceptable.
        if settings.ENVIRONMENT in ("dev", "test"):
            return _base_response("ok")
        # In staging/production, a missing database URL is a failure.
        return JSONResponse(
            status_code=503,
            content={"status": "not ready", "reason": "database not configured"},
        )

    if check_database_connection():
        return _base_response("ok")

    return JSONResponse(
        status_code=503,
        content={"status": "not ready", "reason": "database unreachable"},
    )
