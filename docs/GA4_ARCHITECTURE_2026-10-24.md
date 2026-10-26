# GA4 Discovery & Target Architecture — updated 2026-10-26

**Project:** Dr. Farah VIP Urgent Care  
**Roadmap item:** P2.2 Resolve GA4 access / property architecture  
**Status:** METADATA RESOLVED / TAG DEPLOYMENT GATED — clinic property/access and production stream identifiers are now known; Google tag/event deployment remains gated by healthcare/privacy classification and controlled implementation.

## 1. Verified current state

### FACT — clinic GA4 property is connected

Windsor.ai exposes the correct Dr. Farah GA4 property:

- property ID: `489069776`
- name: `drfarahvipurgentcare.com`
- authorized through the clinic-controlled Google asset workflow

A live data query succeeds but returns **zero events/rows** for the recent period. This is expected because the website does not yet have an approved production GA4 tag/event implementation.

### FACT — production Web stream metadata is now recorded

Owner-provided GA4 Admin metadata on 2026-10-26:

- Web Stream ID: `11211773871`
- Measurement ID: `G-D58FTMF05S`

These identifiers belong to the clinic production GA4 property above. They are configuration metadata, not secrets.

### FACT — unrelated GA4 property remains separate

The Windsor connection also exposes unrelated property `483894121` (`safeguardsupport.com`). It is not part of this project and must never be used as the clinic production property.

### FACT — Google Ads contains legacy GA4 evidence

Google Ads account `652-510-3588` contains the hidden legacy GA4-origin conversion action:

- `drfarahvipurgentcare.com (web) purchase`
- type `GOOGLE_ANALYTICS_4_PURCHASE`
- hidden / not primary
- no recorded conversion date

Treat it as historical configuration evidence only. Do not reuse it as the new conversion model without validation.

### FACT — current website measurement state

Repository/source audit found no implemented Google tag/GTM/GA4 event layer in the inspected frontend. The production assembly does not inject Analytics.

Google Ads exposes tag destination ID:

`AW-17076731177`

Google Ads auto-tagging is enabled.

## 2. Ownership/access decision

GA4 is a clinic-controlled business asset.

Durable model:

- Dr. Farah / clinic retains administrator-level ownership/control;
- Behnam has the access required for measurement operations;
- the correct property is connected to Windsor.ai for project analysis;
- unrelated Behnam properties remain separate.

The access/property-discovery and stream-ID portions of P2.2 are resolved.

## 3. Healthcare/privacy gate

Do **not** deploy GA4 site-wide by default.

Current Google Analytics guidance for HIPAA-regulated entities says they must not use Google Analytics in a way that gives Google access to PHI; authenticated pages are likely HIPAA-covered, and unauthenticated pages related to the provision of healthcare services may also require exclusion. Google does not offer a HIPAA Business Associate Agreement for Google Analytics. See Google Analytics Help: `https://support.google.com/analytics/answer/13297105`.

Google Analytics policies also prohibit sending PII and specifically warn that page URLs/titles, campaign parameters and event dimensions can accidentally carry identifying information. See `https://support.google.com/analytics/answer/6366371`.

Before any production tag deployment:

1. determine whether the clinic is a HIPAA-regulated entity for this implementation and obtain the appropriate legal/privacy classification of eligible pages;
2. do not tag booking, patient-registration, admin, authenticated or other patient-workflow pages by default;
3. do not send names, email, phone, reason for visit, symptoms, diagnosis, medications, treatment, test results or other clinical detail;
4. avoid sending health intent through page URL/title, event names/parameters, custom dimensions or campaign parameters;
5. keep Enhanced Measurement off initially unless individual features are reviewed and approved;
6. use **basic consent mode** if Google measurement is later enabled, so Google tags do not load or transmit data before the user grants measurement consent;
7. align the privacy/cookie/tracking disclosure with the actual implementation.

The project should maximize useful lawful/platform-compliant measurement, but not by forcing patient/health data into Google systems.

## 4. First-party attribution is the durable foundation

The core business attribution path does not depend on GA4 observing healthcare pages.

Target:

`marketing source/click ID → first-party attribution → appointment → status=completed → visit_completed → approved Ads/reporting import`

The structured first-party attribution implementation preserves only non-clinical acquisition metadata such as:

- canonical source;
- UTM source/medium/campaign/content/term;
- GCLID / GBRAID / WBRAID where present;
- partner/referral code;
- explicit traveler segment marker;
- opaque marketing-session ID;
- first-touch and useful last-touch context.

It does not store page/service/medical-intent context inside the marketing attribution record merely because that information is available elsewhere.

## 5. Production vs staging

Production measurement must not be polluted by staging traffic.

Rules:

- no production GA4/Ads events from staging;
- any future Google tag inclusion must be explicit and hostname/environment aware;
- first-party attribution may be tested on staging without sending production Google events;
- production deployment continues through normal Git/Jenkins controls.

## 6. Google tag architecture after privacy approval

For pages/events explicitly cleared for Google measurement, prefer the smallest repository-controlled implementation:

- direct Google tag / small analytics wrapper initially;
- Measurement ID `G-D58FTMF05S` only in production and only on approved pages;
- basic consent mode: do not load the Google tag until measurement consent is granted;
- no duplicate GA4 + Ads tag footprints;
- explicit environment and page allowlist controls;
- GTM only if a concrete operational need later justifies it.

The relationship between GA4 property `489069776`, Web Stream ID `11211773871`, Measurement ID `G-D58FTMF05S`, and Google Ads destination `AW-17076731177` must be validated before production activation.

## 7. Measurement model

### Diagnostic

Use only safe events that answer a real analysis question and do not expose patient/health detail.

### Secondary lead signal

`booking_request_created` remains a first-party business event. It should not be shared with Google unless an approved implementation can do so without inappropriate patient/health disclosure.

### Primary business outcome

`visit_completed` is the intended optimization outcome, derived from the authoritative appointment status rather than a browser thank-you page.

The initial privacy-safe read model uses the stable scheduled visit timestamp as `occurred_at`, keeps a deduplication key based on appointment ID, and joins only non-clinical acquisition identifiers from `appointment_attributions`. No PII/PHI is included in the marketing outcome row.

## 8. Current P2.2 completion status

Completed:

- clinic-controlled GA4 property exists;
- authorized access is confirmed;
- property ID `489069776` recorded;
- Web Stream ID `11211773871` recorded;
- Measurement ID `G-D58FTMF05S` recorded;
- Windsor/project access works;
- recent GA4 data query is reachable;
- production/staging principle documented;
- healthcare/privacy gate documented;
- first-party attribution foundation merged to `dev` after successful Jenkins validation.

Still needed before P2.2 can be marked DONE:

- confirm timezone/currency/Enhanced Measurement settings in the live property;
- obtain the appropriate legal/privacy classification for any pages proposed for Google measurement;
- understand/confirm GA4 ↔ Google Ads destination/link relationship;
- validate one safe test event/pageview only after deployment is approved.

## 9. Immediate next actions

1. validate the merged first-party attribution foundation on staging;
2. build and validate the privacy-safe `visit_completed` read model from `Appointment.status == completed`;
3. keep Google tag deployment blocked until page/event eligibility is approved;
4. once approved, implement a production-only page allowlist + basic consent loader for `G-D58FTMF05S`;
5. validate no duplicate events and no unintended sensitive data;
6. build the controlled Google Ads offline-conversion import path from eligible `visit_completed` rows.
