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

    # --- SMTP ---
    # For reservation notification emails.
    # When SMTP_TEST_MODE=true, emails are logged instead of sent.
    SMTP_HOST: str = Field(default="")
    SMTP_PORT: int = Field(default=587)
    SMTP_USER: str = Field(default="")
    SMTP_PASSWORD: str = Field(default="")
    SMTP_FROM: str = Field(default="noreply@drfarah.proxbenovh.cloud")
    SMTP_TO: str = Field(default="appointments@drfarah.proxbenovh.cloud")
    SMTP_USE_TLS: bool = Field(default=True)
    SMTP_TEST_MODE: bool = Field(default=True)

    # --- Keycloak / OIDC ---
    # Non-secret values; safe in ConfigMap.
    KEYCLOAK_ISSUER: str = Field(
        default="https://keycloak.soria-academie.fr/realms/drfarah"
    )
    KEYCLOAK_JWKS_URL: str = Field(
        default="https://keycloak.soria-academie.fr/realms/drfarah/protocol/openid-connect/certs"
    )
    KEYCLOAK_AUDIENCE: str = Field(
        default="drfarah-admin"
    )
    # Keycloak public clients often omit the standard "aud" claim and rely on
    # "azp" (authorized party) instead.  Start lenient and enforce azp match
    # only when this flag is explicitly turned on.
    KEYCLOAK_VERIFY_AUD: bool = Field(default=False)

    # --- Internal operations ---
    CLEANUP_TOKEN: str = Field(
        default="",
        description="Pre-shared token for the CI cleanup internal endpoint",
    )

    @property
    def cleanup_token(self) -> str:
        return self.CLEANUP_TOKEN


@lru_cache
def get_settings() -> Settings:
    return Settings()
