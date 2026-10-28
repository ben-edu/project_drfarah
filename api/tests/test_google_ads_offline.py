import datetime

import pytest

from app.services.google_ads_offline import prepare_visit_completed_ingest


def _row(**overrides):
    row = {
        "outcome_key": "visit_completed:123",
        "event_name": "visit_completed",
        "occurred_at": datetime.datetime(
            2026, 10, 26, 16, 30, tzinfo=datetime.timezone.utc
        ),
        "source": "google_ads",
        "gclid": "gclid-123",
        "gbraid": None,
        "wbraid": None,
        "marketing_session_id": "mkt-session-private",
        "partner_code": "hotel-001",
        "traveler_segment": "yes",
        "attribution_version": "v1",
    }
    row.update(overrides)
    return row


def test_prepares_direct_google_ads_destination_and_dedup_key():
    batch = prepare_visit_completed_ingest(
        [_row()],
        customer_id="652-510-3588",
        conversion_action_id="123456789",
    )

    assert batch.payload["validateOnly"] is True
    assert batch.payload["destinations"] == [
        {
            "operatingAccount": {
                "accountId": "6525103588",
                "accountType": "GOOGLE_ADS",
            },
            "loginAccount": {
                "accountId": "6525103588",
                "accountType": "GOOGLE_ADS",
            },
            "productDestinationId": "123456789",
        }
    ]

    event = batch.payload["events"][0]
    assert event == {
        "transactionId": "visit_completed:123",
        "eventTimestamp": "2026-10-26T16:30:00Z",
        "eventSource": "OTHER",
        "adIdentifiers": {"gclid": "gclid-123"},
    }
    assert batch.eligible_outcome_keys == ("visit_completed:123",)
    assert batch.skipped_outcome_keys == ()


def test_skips_completed_outcome_without_google_click_identifier():
    batch = prepare_visit_completed_ingest(
        [_row(gclid=None, gbraid=None, wbraid=None)],
        customer_id="6525103588",
        conversion_action_id="123456789",
    )

    assert batch.payload["events"] == []
    assert batch.eligible_outcome_keys == ()
    assert batch.skipped_outcome_keys == ("visit_completed:123",)


def test_emits_only_one_click_identifier_and_prefers_web_identifiers():
    batch = prepare_visit_completed_ingest(
        [_row(gclid="g", wbraid="w", gbraid="b")],
        customer_id="6525103588",
        conversion_action_id="123456789",
    )
    assert batch.payload["events"][0]["adIdentifiers"] == {"gclid": "g"}

    batch = prepare_visit_completed_ingest(
        [_row(gclid=None, wbraid="w", gbraid="b")],
        customer_id="6525103588",
        conversion_action_id="123456789",
    )
    assert batch.payload["events"][0]["adIdentifiers"] == {"wbraid": "w"}


def test_does_not_forward_patient_or_internal_marketing_context():
    batch = prepare_visit_completed_ingest(
        [
            _row(
                email="private@example.com",
                phone="+13105550199",
                reason_category="Private health detail",
            )
        ],
        customer_id="6525103588",
        conversion_action_id="123456789",
    )

    serialized = repr(batch.payload)
    assert "private@example.com" not in serialized
    assert "+13105550199" not in serialized
    assert "Private health detail" not in serialized
    assert "mkt-session-private" not in serialized
    assert "hotel-001" not in serialized
    assert "traveler" not in serialized


def test_rejects_naive_conversion_timestamp():
    with pytest.raises(ValueError, match="timezone"):
        prepare_visit_completed_ingest(
            [_row(occurred_at=datetime.datetime(2026, 10, 26, 16, 30))],
            customer_id="6525103588",
            conversion_action_id="123456789",
        )


def test_supports_manager_login_account_without_changing_operating_account():
    batch = prepare_visit_completed_ingest(
        [_row()],
        customer_id="6525103588",
        login_customer_id="123-456-7890",
        conversion_action_id="123456789",
        validate_only=False,
    )

    destination = batch.payload["destinations"][0]
    assert destination["operatingAccount"]["accountId"] == "6525103588"
    assert destination["loginAccount"]["accountId"] == "1234567890"
    assert batch.payload["validateOnly"] is False
