"""Application configuration — environment-based.

All sensitive values come from the environment (ConfigMap + Secret in K8s).
No secrets are hard-coded here.

For local development, create a .env file (git-ignored) or set env vars.
"""

from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # --- Application ---
    APP_NAME: str = Field(default="drfarah-api")
    ENVIRONMENT: str = Field(default="dev")  # dev | staging | prod
    LOG_LEVEL: str = Field(default="INFO")

    # --- Database ---
    # In staging/production, DATABASE_URL is set from a K8s Secret.
    # In tests, it is overridden to SQLite.
    DATABASE_URL: Optional[str] = Field(default=None)

    @property
    def effective_database_url(self) -> str | None:
        """Explicit URL, or None (meaning no database configured)."""
        return self.DATABASE_URL

    # --- CORS ---
    # Comma-separated list of allowed origins.
    # Staging origins must not include production origins.
    CORS_ORIGINS: str = Field(
        default="https://staging.drfarah.proxbenovh.cloud"
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]

    # --- Trusted proxy ---
    # In production/staging, requests arrive through Traefik and HAProxy.
    # Trust the X-Forwarded-* headers from the cluster network.
    TRUST_PROXY: bool = Field(default=False)


@lru_cache
def get_settings() -> Settings:
    return Settings()
