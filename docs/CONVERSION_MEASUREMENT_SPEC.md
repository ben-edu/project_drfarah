# Canonical Conversion Measurement Specification

**Project:** Dr. Farah VIP Urgent Care  
**Version:** 1.0 — implementation target  
**Date:** 2026-10-24  
**Applies to:** website, booking/admin, GA4, Google Ads, attribution and future Growth Intelligence

## 1. Purpose

Define one stable measurement vocabulary that distinguishes website behavior from real business outcomes and supports direct optimization toward completed visits as soon as the linkage is technically reliable.

Business ladder:

`Visit → Qualified Contact → Appointment Request → Confirmed Appointment → Completed Visit → Collected Revenue → Contribution / Repeat / Referral Value`

No platform event should be described as a patient outcome unless it actually represents that outcome.

## 2. Core rules

1. A page view is not a lead.
2. A phone click is not a qualified call.
3. An appointment request is not a confirmed appointment.
4. A confirmed appointment is not a completed visit.
5. A Google Ads conversion is not automatically a completed patient.
6. Diagnostic events may exist for analysis without becoming Ads primary conversions.
7. The intended primary Google Ads business-outcome conversion is `visit_completed` once end-to-end linkage/import passes validation.
8. `booking_request_created` is a lead/secondary signal, not the desired optimization endpoint.
9. Use useful lawful/platform-compliant measurement; do not impose arbitrary data restrictions, but exclude unnecessary clinical-record detail from marketing systems.
10. Staging must never pollute production analytics or Ads conversions.

## 3. Compact event taxonomy

### Diagnostic website events

Use only where they answer a real funnel/UX question:

- `landing_view`
- `primary_cta_click`
- `booking_start`
- `availability_viewed`
- `slot_selected`
- `booking_request_failed`
- `click_to_call`

Additional diagnostic events may be added only when they improve a defined analysis or implementation check.

### Lead signal

`booking_request_created`

Trigger only after the public booking API successfully creates the pending appointment.

Meaning:

- booking request exists;
- appointment is initially pending;
- not a confirmed visit;
- useful as a secondary/backup Ads signal and funnel KPI.

### Business outcomes

- `appointment_confirmed`
- `visit_completed`
- `appointment_cancelled`
- `appointment_no_show`
- `collected_revenue` when approved/available

The current appointment model already supports pending/confirmed/cancelled/completed/no-show states, so completed-visit measurement should reuse existing operational truth rather than invent a second outcome state.

## 4. Google Ads conversion hierarchy

### Target architecture

**Primary:**

- `visit_completed`

**Secondary / observation:**

- `booking_request_created`
- `appointment_confirmed` where useful
- qualified/connected call when reliably measurable
- selected diagnostic signals only if they do not distort bidding

Do not make page views, CTA clicks, booking starts, directions or generic call clicks primary merely to increase reported conversion volume.

### Transitional rule

If `visit_completed` cannot yet be imported reliably, do not rush paid relaunch using a misleading primary conversion.

A bounded test may temporarily use the strongest reliable intermediate signal only when:

- the limitation is documented;
- the Ads experiment explicitly acknowledges the weaker optimization target;
- a plan/date exists to complete `visit_completed` linkage;
- business outcome review remains external to platform conversions.

## 5. `visit_completed` linkage contract

Target flow:

`acquisition/session → booking attribution → appointment → status=completed → conversion import/reporting`

Minimum requirements:

- preserve acquisition identifiers through booking creation;
- link marketing context to appointment using an internal/opaque reference;
- detect first transition to completed state;
- generate a stable conversion/event identifier for deduplication;
- use clinic/business timezone consistently;
- prevent duplicate imports on repeated admin edits;
- define correction behavior if an outcome is later reversed/corrected;
- log import/processing success/failure;
- validate one controlled end-to-end journey before treating it as production-ready.

## 6. Acquisition data to preserve

Where applicable and useful:

- anonymous marketing/session ID;
- first landing page;
- referrer;
- source;
- medium;
- campaign name/ID;
- UTM parameters;
- Google Ads click identifier such as GCLID where applicable;
- explicit partner/referral code;
- first-touch source;
- useful last-non-direct source;
- attribution rule/version;
- opaque booking/appointment linkage key.

Do not overload the existing coarse `appointments.source` field with the full attribution model. Preserve backward compatibility while adding structured attribution where needed.

## 7. Call measurement

Distinguish:

- `click_to_call` — browser interaction only;
- `call_connected` — telephony confirms connection;
- `qualified_call` — non-clinical business qualification;
- `visit_completed` — patient actually seen.

Use the strongest reliable measure; never assume a phone click equals a patient.

## 8. Privacy / data-use boundary

The objective is effective measurement, not artificial restriction.

Potentially appropriate marketing/analytics fields include non-clinical acquisition metadata, page/CTA context, campaign identifiers, technical outcomes, opaque IDs and approved business outcomes.

Do not send unnecessary:

- diagnosis;
- free-text symptoms;
- medications;
- detailed medical history;
- clinical notes;
- lab/test results;
- medical documents;
- insurance/member identifiers;
- unrestricted reason-for-visit text.

Direct identifiers such as email/phone may only be used in a marketing measurement feature if the specific implementation is lawful, platform-compliant, intentionally approved and documented. Do not assume they are prohibited in every measurement design, and do not enable them casually.

## 9. Environment rules

### Production

Approved production analytics/Ads measurement may operate after implementation/privacy validation.

### Staging

Staging must not create production GA4/Ads conversions.

Use explicit environment isolation such as separate stream/property, production-only injection, hostname conditions, GTM environment separation or another documented equivalent.

## 10. GA4 role

GA4 should support:

- acquisition source/medium/campaign analysis;
- landing-page performance;
- diagnostic funnel behavior;
- lead/booking signals;
- measurement QA;
- cross-checking attribution quality.

GA4 is not the final authority for completed patient outcome unless the event is generated from reliable operational outcome data.

## 11. Google Ads / offline outcome role

The Ads system should receive `visit_completed` through the most appropriate supported import/measurement path after implementation review.

The design should support:

- correct click/source linkage;
- deduplication;
- conversion time integrity;
- outcome validation;
- error monitoring;
- later value optimization only when collected revenue/contribution linkage is defensible.

Do not fabricate monetary conversion values.

## 12. Acceptance criteria for `G2-MEASUREMENT-READY`

All must be true:

1. production/staging measurement isolation is proven;
2. correct GA4 property/data stream is known and accessible;
3. source/UTM/ad-click context survives the intended booking path;
4. successful booking request produces the intended lead signal;
5. appointment completion can produce one deduplicated `visit_completed` outcome;
6. Google Ads receives or is demonstrably ready to receive the completed-visit conversion through the approved implementation;
7. no duplicate firing/import occurs in the controlled test;
8. no unintended clinical-record detail appears in marketing payloads;
9. privacy/cookie/tracking copy is aligned with actual implementation;
10. validation evidence is recorded in GitHub/handoff.

## 13. Reporting standard

Report separately:

- diagnostic funnel rates;
- booking requests;
- confirmed appointments;
- completed visits;
- completed-visit rate from paid/organic/referral sources;
- defensible CAC per completed visit where spend/source linkage exists;
- revenue/contribution only where data quality supports it.

The central optimization question is not “how many conversions did Google report?” but:

> Which acquisition activity produced completed visits at acceptable business value?
