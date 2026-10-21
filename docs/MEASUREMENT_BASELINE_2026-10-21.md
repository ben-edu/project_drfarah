# Production Measurement Baseline — 2026-10-21

**Project:** Dr. Farah VIP Urgent Care  
**Scope:** P0.2 — inventory current site measurement stack  
**Repository:** `ben-edu/project_drfarah`  
**Evidence branch inspected:** `dev` plus production branch source where noted  
**Purpose:** establish what measurement exists before any Google Ads launch or analytics implementation.

## Executive finding

The current repository does **not** contain an implemented Google measurement stack.

No repository evidence was found for:

- Google tag / `gtag.js`;
- Google Tag Manager;
- GA4 page/event instrumentation;
- Google Ads website conversion tags;
- `dataLayer` event pushes;
- click-to-call analytics;
- booking-funnel analytics events.

The booking application already preserves a **limited first-party acquisition marker**, but it is not a full attribution system.

This means the site is not ready for a meaningful paid-media launch yet. Measurement architecture must be defined and implemented before spend begins.

---

## Evidence reviewed

### Frontend source

Repository-wide code searches on the default branch returned no matches for:

- `googletagmanager`
- `gtag`
- `dataLayer`
- `Google Analytics`
- `analytics`

Key source files reviewed:

- `frontend/index.html`
- `frontend/book.html`
- `frontend/app.js`
- `frontend/booking.js`
- `frontend/privacy.html`

### Production assembly

`scripts/prepare-production-frontend.sh` copies the frontend tree, swaps production robots/Apache policy and removes staging `noindex` metadata. It does not inject analytics, Google Ads tags or Google Tag Manager.

The production branch `frontend/index.html` inspected on 2026-10-21 also contains no Google measurement snippet.

### Booking data model

`frontend/booking.js` accepts:

- `service`
- `reason`
- `source`
- `partner`
- `utm_source`

It collapses acquisition context into a single `source` marker.

`api/app/models/appointment.py` confirms:

`appointments.source = String(32)`

This is useful as a coarse backward-compatible source field, but it is insufficient for durable campaign/session attribution.

---

# Findings

## F-001 — Google tag not implemented

**Classification:** FACT  
**Severity:** HIGH for paid-media readiness

No Google tag implementation was found in repository source or production assembly logic.

### Consequence

Google Ads website conversions and GA4 behavioral/event measurement cannot currently be assumed to work.

### Required action

Define the approved production measurement architecture before installing anything.

---

## F-002 — Google Tag Manager not implemented

**Classification:** FACT  
**Severity:** MEDIUM/HIGH

No GTM container snippet or `dataLayer` implementation was found.

### Interpretation

This does not mean GTM is mandatory. The implementation decision should compare:

- direct Google tag;
- GTM-managed Google tag;
- privacy/consent requirements;
- staging/production isolation;
- future event-management needs.

Do not add both direct tags and GTM in a way that duplicates measurement.

---

## F-003 — Booking funnel has no analytics events

**Classification:** FACT  
**Severity:** HIGH

The booking code has observable business steps but no analytics/event instrumentation.

Current functional milestones available for instrumentation include:

1. booking page loaded;
2. service selected;
3. availability requested/viewed;
4. slot selected;
5. details step reached;
6. review step reached;
7. appointment POST attempted;
8. appointment successfully created after HTTP `201`;
9. booking failure.

### Important business rule

Do not make all of these Google Ads primary conversions.

Most are diagnostic funnel events. `booking_created` is the strongest website-level conversion currently available, but even that is not equal to a completed visit.

---

## F-004 — Click-to-call is not instrumented

**Classification:** FACT  
**Severity:** MEDIUM/HIGH

The website contains many `tel:+13104670101` links. `frontend/app.js` modifies some phone CTA labels but does not measure clicks.

### Required action

Define one canonical click-to-call event and record page/context without clinical detail.

A phone click remains a diagnostic/lead event, not a completed patient outcome.

---

## F-005 — Existing attribution is coarse and lossy

**Classification:** FACT  
**Severity:** HIGH for long-term attribution

Current booking attribution logic preserves only one 32-character marker.

Current precedence is:

1. `partner` → `hotel:<partner>`
2. explicit `source`
3. `utm_source` → `utm:<source>`
4. fallback `web`

The current implementation does **not** durably preserve separate structured values for:

- `utm_medium`;
- `utm_campaign`;
- `utm_term`;
- `utm_content`;
- Google Ads click ID where permitted/appropriate;
- first landing page;
- referrer;
- first touch;
- last non-direct touch;
- anonymous marketing-session identifier.

### Required action

Keep `appointments.source` for backward compatibility, but do not expand it into the long-term attribution system.

Use the approved Growth Intelligence direction: structured first-party attribution linked to booking through an opaque reference, without copying unnecessary patient data into marketing tables.

---

## F-006 — Staging and production measurement isolation is not yet designed

**Classification:** FACT / DESIGN GAP  
**Severity:** HIGH

The same frontend source is used for staging and production. Production assembly currently changes crawlability but not analytics configuration.

If a Google tag is added directly to shared static source without environment controls, staging may contaminate production analytics.

### Required action

The implementation must explicitly prevent staging traffic from entering production GA4/Ads datasets.

Acceptable approaches must be chosen during architecture design, for example:

- production-only tag injection;
- environment-specific measurement IDs;
- GTM environment controls;
- explicit hostname guards.

The final choice has not yet been approved.

---

## F-007 — Privacy/cookie copy currently conflicts with future tracking

**Classification:** FACT  
**Severity:** HIGH governance/compliance dependency

`frontend/privacy.html` currently states that the site uses only essential cookies and does not set advertising or third-party tracking cookies.

The page is also explicitly marked as a draft pending clinic/legal review.

The current cookie banner stores an accept/decline choice in local storage, but no analytics/ad tags are present for that choice to control.

### Consequence

Do not silently add tracking while leaving the current public privacy statement unchanged.

### Required action

Before production analytics/advertising tracking is enabled:

1. define what data will actually be collected;
2. define what tags/cookies will actually be used;
3. determine the consent behavior required for the chosen implementation and applicable rules;
4. update privacy/cookie copy through the clinic/legal approval path;
5. verify that the technical implementation matches the published statement.

This document does not make a legal determination.

---

## F-008 — Current booking source handling is useful and should be preserved during migration

**Classification:** FACT / KEEP

The current `source`, `partner` and `utm_source` support is useful for backward-compatible coarse attribution.

### Decision recommendation

Do not remove it when the structured attribution layer is introduced.

Instead:

`existing appointments.source` + `new structured marketing attribution`

should coexist during migration until reconciliation is proven.

---

# Current readiness assessment

| Area | State | Assessment |
|---|---|---|
| Google tag | MISSING | no implementation found |
| GA4 site instrumentation | MISSING / UNVERIFIED ACCOUNT | no code implementation found; account/property still needs live verification |
| GTM | MISSING | no container code found |
| Google Ads website conversions | NOT READY | no website tag/event path implemented |
| Booking funnel events | MISSING | functional steps exist, analytics events do not |
| Click-to-call event | MISSING | many tel links, no analytics handler |
| Coarse booking source | PRESENT | `appointments.source` + source/partner/utm_source |
| Structured attribution | MISSING | required for durable campaign/business-outcome reconciliation |
| Staging isolation | NOT DESIGNED FOR ANALYTICS | must be explicit before implementation |
| Privacy/cookie alignment | BLOCKING IMPLEMENTATION | current text says no tracking; legal/clinic review needed |
| Paid-media launch | BLOCKED | booking health + measurement readiness gates not green |

---

# Recommended measurement architecture — next design step

This is a recommendation, not yet an implemented decision.

## Layer 1 — First-party marketing session

Create an anonymous session identifier and preserve only business-relevant acquisition context such as:

- landing path;
- referrer;
- source;
- medium;
- campaign;
- term/content when available;
- partner/referral code;
- approved click identifier where appropriate;
- timestamps.

Do not place patient name, email, phone, symptoms, diagnosis, medication or clinical notes in this marketing-session entity.

## Layer 2 — Controlled event vocabulary

Recommended initial diagnostic events:

- `landing_view`
- `primary_cta_click`
- `click_to_call`
- `booking_start`
- `service_selected`
- `availability_viewed`
- `slot_selected`
- `details_started`
- `booking_reviewed`
- `booking_created`

Only keep events that answer a defined business question.

## Layer 3 — Business outcome linkage

Use an opaque internal booking/appointment reference to reconcile:

`marketing source → booking → confirmed → completed → revenue`

without duplicating patient-identifiable clinical data into the marketing layer.

## Layer 4 — Google platform measurement

After privacy/consent and account architecture are approved:

- connect the production measurement destination(s);
- validate page/event firing;
- designate only appropriate Google Ads conversions as primary;
- keep diagnostic actions secondary where useful;
- later import/reconcile higher-value business outcomes where technically and legally appropriate.

---

# Immediate next work

## P0.3 — Canonical conversion specification

Define for each event/outcome:

- exact name;
- exact trigger;
- diagnostic vs business outcome;
- GA4 role;
- Google Ads primary/secondary/not-imported role;
- parameters allowed;
- privacy restrictions;
- validation method.

## P2.1/P2.2/P2.3 — Parallel account baselines

Safe to continue while booking/Brevo is being resolved:

- verify Google Ads configuration;
- verify Google Business Profile baseline;
- verify whether a production GA4 property already exists;
- obtain correct production Search Console access/property;
- capture current linked-product state.

Do not launch paid traffic yet.

---

# Acceptance state for P0.2

**State:** `VALIDATING`

Repository/source inventory is complete enough to establish that measurement is not implemented in the current codebase.

P0.2 should be marked `DONE` only after a browser/network-level check of the current production site confirms the deployed state and any provider-side tags not represented in Git are ruled out or documented.

Until then, B-002 remains open but narrowed from “unknown measurement stack” to “repository confirms missing implementation; live runtime validation still required.”
