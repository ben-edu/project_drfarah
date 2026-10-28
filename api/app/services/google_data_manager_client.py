"""Guarded Google Data Manager API transport for offline conversions.

Authentication uses Google Application Default Credentials (ADC). Credentials,
refresh tokens, service-account keys, and access tokens must be supplied by the
runtime environment and are never stored in the repository.

The client is deliberately fail-closed: payloads are expected to use
``validateOnly=true``. A caller must explicitly set ``allow_recording=True`` to
send a request that could record a conversion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import google.auth
from google.auth.transport.requests import Request
import httpx

from app.services.google_ads_offline import (
    DATA_MANAGER_INGEST_URL,
    DATA_MANAGER_OAUTH_SCOPE,
    PreparedOfflineConversionBatch,
)


DEFAULT_TIMEOUT_SECONDS = 20.0
DATA_MANAGER_SCOPES = (DATA_MANAGER_OAUTH_SCOPE,)


class GoogleDataManagerError(RuntimeError):
    """Data Manager transport/authentication failure without payload leakage."""


@dataclass(frozen=True)
class DataManagerIngestResult:
    """Small response surface safe for operational handling."""

    status_code: int
    request_id: str | None
    response: dict[str, Any]


def get_adc_access_token() -> str:
    """Resolve and refresh a Data Manager access token using ADC.

    ADC can represent a user credential, service account, or workload identity
    configuration. The credential material itself stays outside the codebase.
    """

    credentials, _project_id = google.auth.default(scopes=DATA_MANAGER_SCOPES)
    credentials.refresh(Request())
    token = credentials.token
    if not token:
        raise GoogleDataManagerError("ADC did not return a Data Manager access token")
    return str(token)


def ingest_prepared_batch(
    batch: PreparedOfflineConversionBatch,
    *,
    access_token: str | None = None,
    allow_recording: bool = False,
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    client: httpx.Client | None = None,
) -> DataManagerIngestResult:
    """Send one prepared Data Manager request with a recording safety gate.

    ``validateOnly=false`` is rejected unless the caller explicitly passes
    ``allow_recording=True``. This prevents a configuration mistake from turning
    a validation command into a live Google Ads conversion upload.

    HTTP error messages intentionally exclude response bodies and request
    payloads so click identifiers are not copied into application logs/errors.
    """

    payload = batch.payload
    events = payload.get("events")
    if not isinstance(events, list) or not events:
        raise GoogleDataManagerError("No eligible visit_completed events to ingest")

    validate_only = payload.get("validateOnly") is True
    if not validate_only and not allow_recording:
        raise GoogleDataManagerError(
            "Refusing non-validation Data Manager request without allow_recording=True"
        )

    token = access_token or get_adc_access_token()
    if not token:
        raise GoogleDataManagerError("Missing Data Manager access token")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    owns_client = client is None
    http_client = client or httpx.Client(timeout=timeout_seconds)
    try:
        response = http_client.post(
            DATA_MANAGER_INGEST_URL,
            headers=headers,
            json=payload,
        )
    except httpx.HTTPError as exc:
        raise GoogleDataManagerError(
            f"Data Manager request failed before response: {exc.__class__.__name__}"
        ) from exc
    finally:
        if owns_client:
            http_client.close()

    request_id = response.headers.get("x-goog-request-id") or response.headers.get(
        "x-request-id"
    )

    if response.status_code >= 400:
        suffix = f" request_id={request_id}" if request_id else ""
        raise GoogleDataManagerError(
            f"Data Manager returned HTTP {response.status_code}.{suffix}"
        )

    try:
        body = response.json()
    except ValueError as exc:
        raise GoogleDataManagerError(
            f"Data Manager returned non-JSON success response (HTTP {response.status_code})"
        ) from exc

    if not isinstance(body, dict):
        raise GoogleDataManagerError("Data Manager success response must be a JSON object")

    return DataManagerIngestResult(
        status_code=response.status_code,
        request_id=request_id,
        response=body,
    )
