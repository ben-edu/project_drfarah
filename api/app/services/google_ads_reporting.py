"""Read-only Google Ads API v26 reporting, independent of Data Manager uploads."""
from __future__ import annotations
import re
from datetime import date
from typing import Any
import httpx

API_ROOT = "https://googleads.googleapis.com/v26"
ADS_SCOPE = "https://www.googleapis.com/auth/adwords"
CUSTOMER_ID = "6525103588"

class GoogleAdsReadError(RuntimeError):
    """Safe error: never include API response bodies or tokens."""

def customer_id(value: str) -> str:
    result = str(value).replace("-", "").strip()
    if re.fullmatch(r"[0-9]{10}", result) is None:
        raise ValueError("Invalid 10-digit Google Ads customer ID")
    return result

def get_access_token() -> str:
    # Existing production requirements already include google-auth[requests].
    try:
        import google.auth
        from google.auth.transport.requests import Request
    except ImportError as exc:
        raise GoogleAdsReadError("google-auth is not installed") from exc
    credentials, _ = google.auth.default(scopes=(ADS_SCOPE,))
    credentials.refresh(Request())
    if not credentials.token:
        raise GoogleAdsReadError("No Google Ads OAuth access token")
    return str(credentials.token)

def query_for(report: str, start: str | None = None, end: str | None = None) -> str:
    fixed = {
        "account": ("SELECT customer.id, customer.descriptive_name, "
                    "customer.currency_code, customer.time_zone FROM customer LIMIT 1"),
        "campaigns": ("SELECT campaign.id, campaign.name, campaign.status, "
                      "campaign.advertising_channel_type, campaign.bidding_strategy_type, "
                      "campaign.campaign_budget FROM campaign ORDER BY campaign.id"),
        "budgets": ("SELECT campaign_budget.id, campaign_budget.amount_micros, "
                    "campaign_budget.explicitly_shared, campaign_budget.reference_count "
                    "FROM campaign_budget ORDER BY campaign_budget.id"),
        "recommendations": (
            "SELECT recommendation.resource_name, recommendation.type, "
            "recommendation.campaign, recommendation.dismissed, "
            "recommendation.impact, "
            "recommendation.campaign_budget_recommendation "
            "FROM recommendation ORDER BY recommendation.type LIMIT 500"
        ),
        "schedules": (
            "SELECT campaign.id, campaign.name, campaign_criterion.status, "
            "campaign_criterion.ad_schedule.day_of_week, "
            "campaign_criterion.ad_schedule.start_hour, "
            "campaign_criterion.ad_schedule.start_minute, "
            "campaign_criterion.ad_schedule.end_hour, "
            "campaign_criterion.ad_schedule.end_minute "
            "FROM campaign_criterion "
            "WHERE campaign_criterion.type = AD_SCHEDULE "
            "AND campaign_criterion.status = ENABLED "
            "AND campaign.id IN (24414014329, 24404901753, 23637947414)"
        ),
    }
    if report in fixed:
        if start is not None or end is not None:
            raise ValueError("This report does not accept dates")
        return fixed[report]
    if report not in ("daily", "ad_groups", "search_terms", "changes"):
        raise ValueError("Unknown report")
    if start is None or end is None:
        raise ValueError("Start and end dates are required")
    try:
        begin, finish = date.fromisoformat(start), date.fromisoformat(end)
    except ValueError as exc:
        raise ValueError("Dates must be YYYY-MM-DD") from exc
    if begin > finish:
        raise ValueError("Start date must precede end date")
    if report == "changes":
        if (finish - begin).days >= 30:
            raise ValueError("Change Event query must cover fewer than 30 days")
        return ("SELECT change_event.change_date_time, change_event.client_type, "
                "change_event.change_resource_type, change_event.user_email, "
                "change_event.resource_name, change_event.change_resource_name "
                "FROM change_event WHERE change_event.change_date_time >= "
                f"'{begin} 00:00:00' AND change_event.change_date_time <= "
                f"'{finish} 23:59:59' ORDER BY change_event.change_date_time DESC LIMIT 5000")
    period = f"segments.date BETWEEN '{begin}' AND '{finish}'"
    if report == "daily":
        return ("SELECT campaign.id, campaign.name, segments.date, metrics.impressions, "
                "metrics.clicks, metrics.cost_micros, metrics.conversions, "
                "metrics.all_conversions, metrics.phone_calls FROM campaign WHERE "
                + period + " ORDER BY segments.date, campaign.id")
    if report == "ad_groups":
        return ("SELECT campaign.id, ad_group.id, ad_group.name, ad_group.status, "
                "ad_group.cpc_bid_micros, metrics.impressions, metrics.clicks, "
                "metrics.cost_micros, metrics.conversions FROM ad_group WHERE "
                + period + " ORDER BY campaign.id, ad_group.id")
    return ("SELECT campaign.id, ad_group.id, search_term_view.search_term, "
            "metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions "
            "FROM search_term_view WHERE " + period +
            " AND metrics.impressions > 0 ORDER BY metrics.cost_micros DESC LIMIT 5000")

def read_report(
    *, report: str, start: str | None = None, end: str | None = None,
    ads_customer_id: str = CUSTOMER_ID, login_customer_id: str | None = None,
    token: str | None = None, client: httpx.Client | None = None,
    max_rows: int = 10000,
) -> list[dict[str, Any]]:
    """Calls only GoogleAdsService.SearchStream; never mutate or import conversions."""
    query = query_for(report, start, end)
    if not 1 <= max_rows <= 50000:
        raise ValueError("max_rows outside supported range")
    account = customer_id(ads_customer_id)
    manager = customer_id(login_customer_id) if login_customer_id else None
    auth = token or get_access_token()
    if not auth:
        raise GoogleAdsReadError("Missing OAuth token")
    headers = {"Authorization": "Bearer " + auth, "Content-Type": "application/json"}
    if manager:
        headers["login-customer-id"] = manager
    own = client is None
    transport = client or httpx.Client(timeout=35.0)
    try:
        response = transport.post(
            API_ROOT + "/customers/" + account + "/googleAds:searchStream",
            headers=headers, json={"query": query},
        )
    except httpx.HTTPError as exc:
        raise GoogleAdsReadError("Ads transport failed: " + type(exc).__name__) from None
    finally:
        if own:
            transport.close()
    request_id = response.headers.get("request-id")
    if response.status_code >= 400:
        raise GoogleAdsReadError(
            "Google Ads HTTP " + str(response.status_code) +
            (" request-id=" + request_id if request_id else "")
        )
    try:
        batches = response.json()
    except ValueError:
        raise GoogleAdsReadError("Invalid SearchStream JSON") from None
    if not isinstance(batches, list):
        raise GoogleAdsReadError("Unexpected SearchStream envelope")
    rows = []
    for batch in batches:
        if not isinstance(batch, dict) or not isinstance(batch.get("results", []), list):
            raise GoogleAdsReadError("Unexpected SearchStream batch")
        for row in batch.get("results", []):
            if not isinstance(row, dict):
                raise GoogleAdsReadError("Unexpected SearchStream row")
            rows.append(row)
            if len(rows) > max_rows:
                raise GoogleAdsReadError("Too many rows; narrow the date interval")
    return rows
