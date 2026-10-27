import datetime

import httpx
import pytest

from app.services.google_ads_offline import prepare_visit_completed_ingest
from app.services.google_data_manager_client import (
    DATA_MANAGER_INGEST_URL,
    GoogleDataManagerError,
    get_adc_access_token,
    ingest_prepared_batch,
)


def _batch(*, validate_only=True, gclid="gclid-safe-test"):
    return prepare_visit_completed_ingest(
        [
            {
                "outcome_key": "visit_completed:123",
                "event_name": "visit_completed",
                "occurred_at": datetime.datetime(
                    2026, 10, 27, 18, 30, tzinfo=datetime.timezone.utc
                ),
                "gclid": gclid,
                "gbraid": None,
                "wbraid": None,
            }
        ],
        customer_id="6525103588",
        conversion_action_id="123456789",
        validate_only=validate_only,
    )


def test_validate_only_request_posts_expected_payload_and_auth_header():
    seen = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen["method"] = request.method
        seen["url"] = str(request.url)
        seen["authorization"] = request.headers["Authorization"]
        seen["body"] = request.read().decode("utf-8")
        return httpx.Response(
            200,
            headers={"x-goog-request-id": "req-123"},
            json={"requestId": "ingest-123"},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    result = ingest_prepared_batch(
        _batch(),
        access_token="access-token-secret",
        client=client,
    )

    assert seen["method"] == "POST"
    assert seen["url"] == DATA_MANAGER_INGEST_URL
    assert seen["authorization"] == "Bearer access-token-secret"
    assert '"validateOnly":true' in seen["body"].replace(" ", "")
    assert result.status_code == 200
    assert result.request_id == "req-123"
    assert result.response == {"requestId": "ingest-123"}


def test_rejects_recording_request_without_explicit_gate():
    with pytest.raises(GoogleDataManagerError, match="allow_recording=True"):
        ingest_prepared_batch(
            _batch(validate_only=False),
            access_token="token",
        )


def test_allows_recording_request_only_when_explicitly_enabled():
    def handler(request: httpx.Request) -> httpx.Response:
        assert b'"validateOnly":false' in request.read().replace(b" ", b"")
        return httpx.Response(200, json={"requestId": "recorded-1"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    result = ingest_prepared_batch(
        _batch(validate_only=False),
        access_token="token",
        allow_recording=True,
        client=client,
    )
    assert result.response["requestId"] == "recorded-1"


def test_refuses_batch_with_no_google_click_identifier():
    empty_batch = prepare_visit_completed_ingest(
        [
            {
                "outcome_key": "visit_completed:999",
                "event_name": "visit_completed",
                "occurred_at": datetime.datetime(
                    2026, 10, 27, 18, 30, tzinfo=datetime.timezone.utc
                ),
                "gclid": None,
                "gbraid": None,
                "wbraid": None,
            }
        ],
        customer_id="6525103588",
        conversion_action_id="123456789",
    )
    with pytest.raises(GoogleDataManagerError, match="No eligible"):
        ingest_prepared_batch(empty_batch, access_token="token")


def test_http_error_does_not_echo_click_id_or_response_body():
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400,
            headers={"x-goog-request-id": "req-error"},
            json={"error": "bad gclid gclid-safe-test"},
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    with pytest.raises(GoogleDataManagerError) as exc_info:
        ingest_prepared_batch(
            _batch(),
            access_token="token",
            client=client,
        )

    message = str(exc_info.value)
    assert "HTTP 400" in message
    assert "req-error" in message
    assert "gclid-safe-test" not in message
    assert "bad gclid" not in message


def test_adc_access_token_uses_data_manager_scope(monkeypatch):
    class FakeCredentials:
        token = None

        def refresh(self, _request):
            self.token = "adc-token"

    fake_credentials = FakeCredentials()
    seen = {}

    def fake_default(*, scopes):
        seen["scopes"] = tuple(scopes)
        return fake_credentials, "project-id"

    monkeypatch.setattr(
        "app.services.google_data_manager_client.google.auth.default",
        fake_default,
    )

    assert get_adc_access_token() == "adc-token"
    assert seen["scopes"] == ("https://www.googleapis.com/auth/datamanager",)
