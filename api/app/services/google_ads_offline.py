"""Prepare privacy-safe Google Ads Data Manager offline-conversion payloads.

This module intentionally does not authenticate or send anything to Google.
It converts the first-party ``visit_completed`` read model into the smallest
Google Data Manager API payload we can validate safely before enabling a live
uploader.

No patient identity, clinical context, service detail, partner metadata, or
marketing session identifier is forwarded.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Iterable


DATA_MANAGER_INGEST_URL = "https://datamanager.googleapis.com/v1/events:ingest"
DATA_MANAGER_OAUTH_SCOPE = "https://www.googleapis.com/auth/datamanager"


@dataclass(frozen=True)
class PreparedOfflineConversionBatch:
    """Prepared Data Manager request plus explicit eligibility accounting."""

    payload: dict[str, Any]
    eligible_outcome_keys: tuple[str, ...]
    skipped_outcome_keys: tuple[str, ...]


def _normalize_customer_id(value: str) -> str:
    customer_id = str(value).replace("-", "").strip()
    if not customer_id.isdigit() or len(customer_id) != 10:
        raise ValueError("Google Ads customer id must contain exactly 10 digits")
    return customer_id


def _normalize_conversion_action_id(value: str) -> str:
    action_id = str(value).strip()
    if not action_id.isdigit():
        raise ValueError("Google Ads conversion action id must be numeric")
    return action_id


def _rfc3339(value: datetime) -> str:
    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("visit_completed occurred_at must include a timezone")
    normalized = value.astimezone(timezone.utc).replace(microsecond=0)
    return normalized.isoformat().replace("+00:00", "Z")


def _preferred_ad_identifier(row: dict[str, Any]) -> dict[str, str] | None:
    """Return one click identifier without forwarding unrelated fields.

    GCLID is preferred for normal web clicks. WBRAID is preferred over GBRAID
    when GCLID is absent because the clinic conversion journey is web-based.
    The read model may retain multiple identifiers defensively; the outbound
    event deliberately emits only one.
    """

    for key in ("gclid", "wbraid", "gbraid"):
        value = row.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return {key: text}
    return None


def prepare_visit_completed_ingest(
    rows: Iterable[dict[str, Any]],
    *,
    customer_id: str,
    conversion_action_id: str,
    login_customer_id: str | None = None,
    validate_only: bool = True,
) -> PreparedOfflineConversionBatch:
    """Build one Google Data Manager ``events.ingest`` request.

    Only rows with ``event_name == 'visit_completed'`` and a supported Google
    click identifier are eligible. Rows without a click identifier remain valid
    business outcomes but are skipped for this click-id-based import.

    ``transactionId`` is the existing deterministic outcome key, giving Google
    an idempotent deduplication key without exposing patient identity.
    """

    operating_customer_id = _normalize_customer_id(customer_id)
    login_id = _normalize_customer_id(login_customer_id or customer_id)
    destination_id = _normalize_conversion_action_id(conversion_action_id)

    destination = {
        "operatingAccount": {
            "accountId": operating_customer_id,
            "accountType": "GOOGLE_ADS",
        },
        "loginAccount": {
            "accountId": login_id,
            "accountType": "GOOGLE_ADS",
        },
        "productDestinationId": destination_id,
    }

    events: list[dict[str, Any]] = []
    eligible: list[str] = []
    skipped: list[str] = []

    for row in rows:
        if row.get("event_name") != "visit_completed":
            raise ValueError("offline import accepts only visit_completed rows")

        outcome_key = str(row.get("outcome_key") or "").strip()
        if not outcome_key.startswith("visit_completed:"):
            raise ValueError("visit_completed row is missing a valid outcome_key")

        occurred_at = row.get("occurred_at")
        if not isinstance(occurred_at, datetime):
            raise ValueError("visit_completed occurred_at must be a datetime")

        ad_identifier = _preferred_ad_identifier(row)
        if ad_identifier is None:
            skipped.append(outcome_key)
            continue

        events.append(
            {
                "transactionId": outcome_key,
                "eventTimestamp": _rfc3339(occurred_at),
                "eventSource": "OTHER",
                "adIdentifiers": ad_identifier,
            }
        )
        eligible.append(outcome_key)

    payload = {
        "destinations": [destination],
        "events": events,
        "validateOnly": bool(validate_only),
    }

    return PreparedOfflineConversionBatch(
        payload=payload,
        eligible_outcome_keys=tuple(eligible),
        skipped_outcome_keys=tuple(skipped),
    )
