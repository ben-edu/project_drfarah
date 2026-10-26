# GA4 Discovery & Target Architecture — updated 2026-10-26

**Project:** Dr. Farah VIP Urgent Care  
**Roadmap item:** P2.2 Resolve GA4 access / property architecture  
**Status:** IN_PROGRESS — clinic property/access is now resolved and connected; tag/event deployment remains gated by healthcare/privacy classification and controlled implementation.

## 1. Verified current state

### FACT — clinic GA4 property now exists and is connected

Windsor.ai now exposes the correct Dr. Farah GA4 property:

- property ID: `489069776`
- name: `drfarahvipurgentcare.com`
- authorized through the clinic-controlled Google asset workflow

A live data query succeeds but returns **zero events/rows** for the recent period. This is expected because the website does not yet have an approved production GA4 tag/event implementation.

The exact production Web stream ID and `G-...` measurement ID are not yet visible in the Windsor report data and must be recorded from GA4/admin metadata before tag deployment. Do not guess these IDs.

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

The access/property-discovery portion of P2.2 is therefore resolved.

## 3. Healthcare/privacy gate

Do **not** deploy GA4 site-wide by default.

For a US medical clinic, Google Analytics must not receive PII/PHI or sensitive healthcare context that is unnecessary for analytics. Before deployment:

1. classify which public pages/events, if any, are appropriate for Google measurement;
2. do not tag booking/admin/authenticated workflows by default;
3. do not send names, email, phone, reason for visit, symptoms, diagnosis, medications, treatment, test results or other clinical detail;
4. avoid sending health intent through event names/parameters, custom dimensions or campaign parameters;
5. keep Enhanced Measurement off initially unless individual features are reviewed and approved;
6. align the privacy/cookie/tracking disclosure with the actual implementation.

The project should maximize useful lawful/platform-compliant measurement, but not by forcing patient/health data into Google systems.

## 4. First-party attribution is the durable foundation

The core business attribution path should not depend on GA4 being able to observe every healthcare page.

Target:

`marketing source/click ID → first-party attribution → appointment → status=completed → visit_completed → approved Ads/reporting import`

The structured first-party attribution implementation should preserve only non-clinical acquisition metadata such as:

- canonical source;
- UTM source/medium/campaign/content/term;
- GCLID / GBRAID / WBRAID where present;
- partner/referral code;
- explicit traveler segment marker;
- opaque marketing-session ID;
- first-touch and useful last-touch context.

It should not store page/service/medical-intent context inside the marketing attribution record merely because that information is available elsewhere.

## 5. Production vs staging

Production measurement must not be polluted by staging traffic.

Rules:

- no production GA4/Ads events from staging;
- any future Google tag inclusion must be explicit and hostname/environment aware;
- first-party attribution may be tested on staging without sending production Google events;
- production deployment continues through normal Git/Jenkins controls.

## 6. Google tag architecture after privacy approval

For pages/events cleared for Google measurement, prefer the smallest repository-controlled implementation:

- direct Google tag / small analytics wrapper initially;
- no duplicate GA4 + Ads tag footprints;
- explicit environment controls;
- GTM only if a concrete operational need later justifies it.

The relationship between GA4 property `489069776`, its future recorded `G-...` measurement ID, and Google Ads destination `AW-17076731177` must be validated before deployment.

## 7. Measurement model

### Diagnostic

Use only safe events that answer a real analysis question and do not expose patient/health detail.

### Secondary lead signal

`booking_request_created` remains a first-party business event. It may be shared with Google only if the approved implementation can do so without inappropriate patient/health disclosure.

### Primary business outcome

`visit_completed` remains the intended optimization outcome, generated from the authoritative appointment status rather than a browser thank-you page.

## 8. Current P2.2 completion status

Completed:

- clinic-controlled GA4 property exists;
- authorized access is confirmed;
- property ID `489069776` recorded;
- Windsor/project access works;
- recent GA4 data query is reachable;
- production/staging principle documented;
- healthcare/privacy gate documented.

Still needed before P2.2 can be marked DONE:

- record exact Web stream ID and `G-...` measurement ID;
- confirm timezone/currency/Enhanced Measurement settings in the live property;
- validate the approved page/event boundary;
- understand/confirm GA4 ↔ Google Ads destination/link relationship;
- validate one safe test event/pageview after deployment is approved.

## 9. Immediate next actions

1. build and validate first-party structured attribution independent of GA4;
2. obtain/record GA4 stream/measurement metadata;
3. classify safe Google-measurement pages/events;
4. implement privacy/consent behavior and the approved Google tag footprint;
5. validate no duplicate events and no unintended sensitive data;
6. continue toward `visit_completed` import/readiness.
