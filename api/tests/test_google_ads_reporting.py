import httpx
import pytest
from app.services.google_ads_reporting import (
    ADS_SCOPE, API_ROOT, GoogleAdsReadError, customer_id, query_for, read_report
)

def test_customer_id():
    assert customer_id("652-510-3588") == "6525103588"
    with pytest.raises(ValueError):
        customer_id("bad")

def test_curated_reports():
    assert "FROM customer" in query_for("account")
    assert "FROM campaign_budget" in query_for("budgets")
    assert "FROM campaign_criterion" in query_for("schedules")
    assert "campaign_criterion.ad_schedule.day_of_week" in query_for("schedules")
    assert "24414014329, 24404901753" in query_for("schedules")
    assert "cost_micros" in query_for("daily", "2026-11-09", "2026-11-15")
    assert "change_event.client_type" in query_for("changes", "2026-11-09", "2026-11-15")
    with pytest.raises(ValueError):
        query_for("changes", "2026-10-01", "2026-11-15")
    with pytest.raises(ValueError):
        query_for("daily", "2026-11-15", "2026-11-09")
    with pytest.raises(ValueError):
        query_for("mutate", "2026-11-09", "2026-11-15")

def test_read_only_endpoint_and_batches():
    seen = {}
    def handler(request):
        seen["url"] = str(request.url)
        seen["method"] = request.method
        seen["header"] = request.headers["login-customer-id"]
        return httpx.Response(200, json=[{"results": [{"customer": {"id": "1"}}]},
                                         {"results": [{"customer": {"id": "2"}}]}])
    with httpx.Client(transport=httpx.MockTransport(handler)) as client:
        result = read_report(
            report="account", token="fake", client=client,
            login_customer_id="111-222-3333"
        )
    assert len(result) == 2
    assert seen["method"] == "POST"
    assert seen["url"] == API_ROOT + "/customers/6525103588/googleAds:searchStream"
    assert seen["header"] == "1112223333"

def test_error_does_not_expose_secrets():
    with httpx.Client(transport=httpx.MockTransport(
        lambda _: httpx.Response(403, headers={"request-id": "safe"}, text="PRIVATE_TOKEN")
    )) as client:
        with pytest.raises(GoogleAdsReadError) as info:
            read_report(report="account", token="secret", client=client)
    assert "HTTP 403" in str(info.value)
    assert "PRIVATE_TOKEN" not in str(info.value)
    assert "secret" not in str(info.value)

def test_bounded_results():
    with httpx.Client(transport=httpx.MockTransport(
        lambda _: httpx.Response(200, json=[{"results": [{}, {}]}])
    )) as client:
        with pytest.raises(GoogleAdsReadError, match="Too many rows"):
            read_report(report="account", token="fake", client=client, max_rows=1)
