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

However, Google tag deployment remains separately gated by healthcare/privacy review. The first-party `visit_completed` outcome exists specifically so the clinic can measure business results even if GA4 cannot appropriately observe healthcare pages.

## 9. Next import step

After this read model passes repository CI and staging validation:

1. inspect Google Ads offline-conversion capabilities and exact deduplication fields;
2. define an approved conversion action for completed visits;
3. export/import only eligible rows with supported click identifiers;
4. never send clinical context or patient identity;
5. reconcile imported conversion counts back to the authoritative first-party outcome count.
