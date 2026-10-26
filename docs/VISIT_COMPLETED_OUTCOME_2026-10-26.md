# `visit_completed` Marketing Outcome Contract — 2026-10-26

**Project:** Dr. Farah VIP Urgent Care  
**Purpose:** define the privacy-safe first-party business outcome used for attribution and future controlled Google Ads offline conversion import.

## 1. Authoritative business state

`visit_completed` is generated only from an appointment whose authoritative application status is:

`completed`

The browser thank-you page, a page view, a phone click, a booking request, a confirmation email, or a Google platform conversion is **not** sufficient to create this outcome.

## 2. Initial implementation

The first implementation is a read model rather than a new event table.

`build_visit_completed_rows(db)` joins:

`appointments` → `appointment_attributions`

and returns one row per appointment whose current status is `completed`.

This gives the project a stable, deduplicated business-outcome dataset without adding another database state machine before it is needed.

## 3. Deduplication

Each row uses:

`visit_completed:<appointment_id>`

as its internal outcome key.

The key is stable across repeated reads and is intended to become the basis for downstream import deduplication. No patient identity is encoded in the key.

## 4. Occurrence time

The initial `occurred_at` value is the appointment's scheduled `starts_at` timestamp.

Reason:

- it is stable;
- it is already authoritative in the scheduling system;
- it avoids using mutable `updated_at` as a conversion timestamp;
- it does not require a new clinical/workflow field merely for advertising measurement.

If the clinic later records a dedicated completion timestamp as part of normal operations, the read model can migrate to that field while keeping the same outcome key.

## 5. Allowed output fields

The read model may contain only non-clinical acquisition/business fields:

- `outcome_key`
- `event_name = visit_completed`
- `occurred_at`
- canonical `source`
- `gclid`
- `gbraid`
- `wbraid`
- `marketing_session_id`
- `partner_code`
- `traveler_segment`
- `attribution_version`

## 6. Explicitly excluded fields

The marketing outcome row must not contain:

- patient first/last name;
- email;
- phone;
- date of birth;
- address;
- reason for visit;
- symptoms;
- diagnosis;
- medications;
- treatment/test details;
- service name/code or other health-intent detail;
- registration or clinical-form content.

The internal database may join the appointment and attribution tables to determine the outcome, but downstream marketing/export records must remain non-clinical.

## 7. Attribution behavior

When attribution exists:

1. prefer `last_touch` for canonical source and click IDs;
2. fall back to `first_touch` when last touch is absent;
3. fall back to the legacy compact `appointments.source` when structured attribution is absent;
4. otherwise use `unknown`.

A completed appointment without a click ID remains a valid business outcome; it simply is not automatically eligible for a click-ID-based Google Ads import.

## 8. Google Analytics / Google Ads boundary

This implementation sends **nothing** to Google.

GA4 production metadata is known:

- property ID `489069776`
- Web Stream ID `11211773871`
- Measurement ID `G-D58FTMF05S`

The selected-page production GA4 wrapper is separate from the business-outcome import. `visit_completed` exists so the clinic can measure completed business outcomes without instrumenting healthcare booking, registration, treatment or clinical pages with detailed Google Analytics events.

## 9. Google Ads/Data Manager import contract

As of 2026-10-26, Google documents the Data Manager API as the preferred current ingestion path for Google Ads offline conversion events.

The controlled import target is:

`POST https://datamanager.googleapis.com/v1/events:ingest`

with OAuth scope:

`https://www.googleapis.com/auth/datamanager`

The destination must point to the Google Ads conversion customer that owns the offline conversion action. For the current clinic account, the operating Google Ads customer is `6525103588`; a manager/login customer may differ if the eventual OAuth credential uses manager-account access.

The conversion action ID is intentionally **not** hard-coded yet because the approved `Visit Completed` offline conversion action has not been created/resolved in Google Ads.

Each eligible outbound event uses only:

- `transactionId = visit_completed:<appointment_id>` for deduplication;
- `eventTimestamp = occurred_at` in RFC 3339 with timezone integrity;
- `eventSource = OTHER` because this is a backend/offline completed-visit outcome rather than a browser event;
- exactly one supported Google click identifier in `adIdentifiers`.

Identifier preference for this web-based clinic journey:

1. `gclid`;
2. `wbraid`;
3. `gbraid`.

Rows with no supported click identifier remain valid first-party completed visits but are skipped by the click-ID importer.

The outbound event deliberately excludes:

- patient identity and contact data;
- health/clinical/service context;
- `marketing_session_id`;
- partner/hotel codes;
- traveler segment;
- source labels not required by the Google destination;
- conversion value until a separately approved business-value policy exists.

The implementation begins with `validateOnly=true` so Google can reject malformed destination/event payloads before any production conversion is recorded.

## 10. Current implementation state

Branch `feature/google-ads-visit-completed-export-20261026` now contains a pure payload-preparation layer:

`api/app/services/google_ads_offline.py`

It does **not** authenticate or transmit data. It prepares the destination/event request, records eligible versus skipped outcome keys, enforces timezone-aware timestamps and strips unrelated internal fields.

Unit tests cover:

- customer/conversion destination construction;
- deterministic transaction IDs;
- RFC 3339 timestamps;
- click-ID preference;
- no-click-ID skip behavior;
- PII/clinical/internal-context non-propagation;
- manager/login-account support;
- validation-only mode.

## 11. Remaining gates before first live import

1. Create or resolve a dedicated Google Ads offline conversion action for completed visits, preferably named `Visit Completed`.
2. Confirm the action is owned by the correct conversion customer and obtain its numeric conversion action ID.
3. Establish a Google Cloud/OAuth credential with Data Manager API access and scope `https://www.googleapis.com/auth/datamanager` without committing credentials to Git.
4. Send a controlled `validateOnly=true` request for a synthetic/test-safe eligible row and inspect request diagnostics.
5. Run one controlled real completed-visit import with a valid click identifier.
6. Re-run the same transaction ID to verify deduplication behavior.
7. Reconcile Google Ads accepted conversion count against the authoritative first-party outcome.
8. Only after that validation, decide whether `Visit Completed` should become a primary bidding conversion.

`G2-MEASUREMENT-READY` remains red until this controlled end-to-end source → appointment → completed visit → accepted Google Ads conversion path passes.