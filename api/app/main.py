"""FastAPI application entry point — Dr. Farah VIP Urgent Care API.

Phase 1: website + booking foundation. No clinical AI.
"""

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers import health

settings = get_settings()

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

# Request body logging is deliberately disabled — patient data must never
# appear in logs. Structured metadata only.
logging.getLogger("uvicorn.access").addFilter(
    lambda record: not any(
        word in record.getMessage().lower()
        for word in ("password", "token", "secret")
    )
)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Dr. Farah VIP Urgent Care API",
        version="0.1.0",
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    # CORS — origins from ConfigMap / environment.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )

    # Trust X-Forwarded-* headers in staging/production (behind HAProxy + Traefik).
    if settings.TRUST_PROXY:
        from fastapi.middleware.trustedhost import TrustedHostMiddleware
        # We don't enable TrustedHostMiddleware here — trusted proxy is handled
        # by uvicorn --proxy-headers flag in production.

    # Health endpoints.
    app.include_router(health.router, prefix="/api/v1/health")

    return app


app = create_app()
