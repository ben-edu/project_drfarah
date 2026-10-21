# Canonical Conversion Measurement Specification

**Project:** Dr. Farah VIP Urgent Care  
**Version:** 0.1 — pre-implementation specification  
**Date:** 2026-10-21  
**Applies to:** website, booking, GA4, Google Ads, attribution, future Growth Intelligence reporting

## 1. Purpose

Define one stable measurement vocabulary before implementing Google tags or launching paid media.

The measurement system must distinguish **diagnostic website behavior** from **real business outcomes**.

The business ladder is:

`Visit → Qualified Contact → Appointment Request → Confirmed Appointment → Completed Visit → Collected Revenue → Contribution / Repeat / Referral Value`

No platform event should be described as a patient outcome unless it actually represents that outcome.

---

## 2. Core rules

1. A page view is not a lead.
2. A phone click is not a qualified call.
3. An appointment request is not a confirmed appointment.
4. A confirmed appointment is not a completed visit.
5. A Google Ads conversion is not automatically a completed patient.
6. Patient-provided clinical or identifiable data must not be sent to marketing platforms merely for attribution.
7. Events must exist because they answer a business question, not because they are technically easy to collect.
8. Google Ads primary conversions should be few, high-value and validated.
9. Diagnostic events may exist in GA4/internal analytics without becoming Ads primary conversions.
10. Long-term optimization should move toward completed visits and defensible business value when data quality permits.

---

# 3. Event taxonomy

## 3.1 Website diagnostic events

| Canonical event | Exact trigger | Role | GA4 | Google Ads | Notes |
|---|---|---|---|---|---|
| `landing_view` | first measured page view of a new first-party marketing session | diagnostic acquisition | yes | no | preserve acquisition context; avoid PII |
| `primary_cta_click` | user clicks a primary Book/Contact CTA | diagnostic intent | yes | no | include CTA type and page only |
| `click_to_call` | user activates clinic `tel:` link | lead signal, not qualified call | yes | secondary only if useful | never equal to completed call/patient |
| `booking_start` | booking flow becomes actively engaged, not merely page loaded | diagnostic funnel | yes | no | recommended trigger: first meaningful booking interaction |
| `service_selected` | user selects a bookable service | diagnostic funnel | internal/GA4 only after privacy review | no | do not transmit sensitive patient-entered health detail |
| `availability_viewed` | availability successfully returned/displayed | diagnostic funnel | yes | no | indicates booking path technically worked |
| `slot_selected` | user selects an available time | diagnostic funnel | yes | no | do not send exact appointment timestamp unless specifically justified |
| `details_started` | user enters booking-details stage | diagnostic funnel | yes | no | no form values in analytics payload |
| `booking_reviewed` | user reaches final review/confirmation stage | diagnostic funnel | yes | no | no PII in analytics payload |
| `booking_request_created` | API returns HTTP 201 for public appointment request | strongest website conversion | yes | **candidate primary** | current appointment starts as `pending`; not confirmed appointment |
| `booking_request_failed` | final appointment request fails | diagnostic quality | yes/internal | no | classify technical failure only; no clinical detail |
| `registration_started` | user begins optional patient registration after booking | diagnostic operations | optional/internal | no | must not send registration fields to marketing tools |

### Important naming correction

The existing planning term `booking_created` is replaced in this specification by
`booking_request_created` because the current API creates an appointment with
status `pending`, and the clinic still needs to confirm it.

This prevents later reports from overstating booking certainty.

---

# 4. Call outcome taxonomy

## `click_to_call`

Browser interaction only.

**Evidence level:** LOW.

## `call_connected`

A call-tracking/telephony source confirms a connected call.

**Evidence level:** MEDIUM.

## `qualified_call`

Clinic-defined non-clinical business qualification indicates the call represents a genuine patient/business opportunity.

**Evidence level:** MEDIUM/HIGH.

Do not place diagnoses, symptoms, medications or clinical call content in marketing qualification fields.

### Ads role

Long-term preference:

`qualified_call` > `call_connected` > `click_to_call`

Use the strongest reliably measurable level.

---

# 5. Booking and visit outcome taxonomy

These are business outcomes, not ordinary browser events.

| Outcome | System meaning | Preferred reporting role | Google Ads long-term role |
|---|---|---|---|
| `appointment_request_created` | booking API created pending appointment | web conversion | initial primary candidate if higher outcomes unavailable |
| `appointment_confirmed` | clinic accepted/confirmed appointment | stronger lead/business outcome | preferred once reliably importable |
| `visit_completed` | patient was actually seen | core acquisition outcome | preferred optimization conversion when volume/data quality permit |
| `appointment_cancelled` | appointment cancelled | negative/operational outcome | not a conversion |
| `appointment_no_show` | patient did not attend | negative/operational outcome | not a conversion |
| `collected_revenue` | approved collected business revenue associated with completed outcome | financial outcome | later value optimization only after governance/data-quality review |

The existing appointment model already supports statuses:

- `pending`
- `confirmed`
- `cancelled`
- `completed`
- `no_show`

This makes confirmed/completed outcome measurement technically plausible without inventing new clinical state.

---

# 6. Initial Google Ads conversion hierarchy

## Phase A — before offline/business-outcome reconciliation

Candidate **primary** conversion:

- validated `booking_request_created`

Potential **secondary** conversions:

- `click_to_call` or connected call, until a stronger qualified-call measure exists;
- other diagnostic actions only when they provide useful reporting and do not distort Smart Bidding.

Do not make these primary merely to increase conversion volume:

- page view;
- CTA click;
- booking start;
- service selection;
- availability view;
- slot selection;
- details start;
- review step.

## Phase B — after business-outcome reconciliation is reliable

Prefer moving bidding/optimization toward:

1. `visit_completed`; or
2. `appointment_confirmed` when completed-visit volume is insufficient;
3. qualified call where phone acquisition is material.

Keep `booking_request_created` as a diagnostic or secondary outcome if a stronger primary becomes reliable.

## Phase C — value optimization

Only after revenue linkage and governance are defensible:

- collected revenue;
- contribution/business value;
- repeat/referral value.

Do not fabricate values for platform optimization.

---

# 7. Allowed event parameters

Keep the initial parameter set minimal.

Potentially allowed non-clinical parameters:

- page path;
- CTA type;
- acquisition source;
- medium;
- campaign identifier/name where appropriate;
- partner/referral code;
- landing path;
- anonymous marketing-session ID in the first-party layer;
- broad environment marker (`production` / `staging`) for internal control;
- technical success/failure category.

Parameters requiring additional privacy/policy review before sending to Google marketing systems:

- detailed service selected;
- reason for visit;
- treatment category where it can reveal sensitive health interest;
- appointment date/time;
- free-text fields;
- any user-entered health information.

Never send as analytics/Ads parameters:

- patient name;
- email;
- phone;
- date of birth;
- address unless a specifically approved minimized use exists;
- symptoms;
- diagnosis;
- medications;
- clinical history;
- insurance/member identifiers;
- lab/test results;
- uploaded medical documents;
- free-text clinical notes.

---

# 8. First-party attribution contract

The existing `appointments.source` field remains a backward-compatible coarse marker.

Do not overload it with the full attribution model.

Long-term structured acquisition context should preserve, where applicable:

- anonymous session ID;
- first landing page;
- referrer;
- first source/medium/campaign;
- last non-direct source/medium/campaign;
- explicit partner/referral code;
- approved ad click identifier when technically/policy appropriate;
- attribution rule/version;
- opaque booking reference.

Recommended relationship:

`marketing_session → controlled events → booking_attribution → opaque booking outcome`

The marketing layer should not become a second patient record.

---

# 9. Environment rules

## Production

Production data may feed approved GA4/Google Ads measurement after privacy/consent review and implementation validation.

## Staging

Staging must not contaminate production analytics or Google Ads conversions.

The implementation must use one or more explicit controls:

- separate measurement property/stream;
- production-only tag injection;
- hostname condition;
- GTM environment/configuration separation;
- another documented equivalent.

A solution that silently sends staging events into production is not acceptable.

---

# 10. Validation requirements

Before `G1-MEASUREMENT-READY` can be green, verify:

1. no duplicate page/event firing;
2. production/staging isolation;
3. no patient form values in marketing payloads;
4. `booking_request_created` fires only after API 201 success;
5. failed appointment creation does not fire success conversion;
6. click-to-call is distinguishable from a connected/qualified call;
7. source/campaign/partner values persist through the intended journey;
8. booking system receives its normal business source marker;
9. GA4/debug tooling receives only approved events/parameters;
10. Google Ads receives only approved conversion actions;
11. published privacy/cookie behavior matches technical behavior.

---

# 11. Implementation order

1. Verify/create the correct production GA4 property/data stream and authorized Google Ads linkage.
2. Approve privacy/cookie/consent behavior for the actual planned tags.
3. Choose direct Google tag vs GTM architecture based on operational needs.
4. Add environment isolation.
5. Implement page/session acquisition capture.
6. Implement diagnostic booking events.
7. Implement `booking_request_created` exactly after successful API response.
8. Implement click-to-call event.
9. Validate in staging without polluting production.
10. Deploy through Jenkins.
11. Validate production browser/network and platform receipts.
12. Only then mark measurement-ready for paid launch.

---

# 12. Current status

**Specification state:** `DRAFT_FOR_VALIDATION`

This specification can be used to design implementation now.

It should be updated when the live Google Ads conversion configuration, GA4 property, call-tracking capability and privacy/consent approach are verified.
