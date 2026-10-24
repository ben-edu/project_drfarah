# GA4 Discovery & Target Architecture — 2026-10-24

**Project:** Dr. Farah VIP Urgent Care  
**Roadmap item:** P2.2 Resolve GA4 access / property architecture  
**Status:** IN_PROGRESS — no reusable Dr. Farah property was found; create a new clinic-controlled production property/data stream, but do not deploy the tag until the healthcare/privacy boundary is approved.

## 1. Verified current state

### FACT — no accessible Dr. Farah GA4 property was found

Windsor.ai initially exposed only:

- property/account ID: `483894121`
- name: `safeguardsupport.com`

The GA4 connector was then re-authorized using the Google account intended for the clinic assets. Owner confirmation on 2026-10-24: **no Dr. Farah property appeared in the property list**.

For current execution, treat this as no reusable clinic GA4 property being available to the project. Do not spend more time trying to recover the legacy property unless new evidence identifies a specific account/property owner.

### FACT — Google Ads contains a legacy GA4-origin conversion action

The live Dr. Farah Google Ads account `652-510-3588` contains a hidden conversion action:

- name: `drfarahvipurgentcare.com (web) purchase`
- origin: `WEBSITE`
- type: `GOOGLE_ANALYTICS_4_PURCHASE`
- status: `HIDDEN`
- primary for goal: `False`
- no recorded last conversion date

This proves that a GA4-origin website conversion was previously configured/imported in Ads. It does **not** prove that the original GA4 property still exists, is clinic-controlled, or is suitable for reuse.

### FACT — repository measurement state

The current repository/source audit found no implemented Google tag, GTM container, GA4 event layer, or booking/call analytics in the inspected frontend source. The production assembly does not inject analytics code.

Google Ads exposes Google tag ID:

`AW-17076731177`

Google Ads auto-tagging is enabled.

## 2. Current decision

Create a **new clinic-controlled GA4 production property and web data stream** for `drfarahvipurgentcare.com`.

Do **not** install the GA4/Google tag on the website yet.

Property/data-stream creation is an account-architecture step only. Tag deployment remains gated by healthcare/privacy review and implementation design.

## 3. Property creation specification

Create under a Google Analytics account controlled by Dr. Farah / the clinic.

Recommended values:

- property name: `Dr Farah VIP Urgent Care - Production`
- reporting timezone: `America/Los_Angeles` / Los Angeles Pacific time
- currency: `USD`
- web stream URL: `https://drfarahvipurgentcare.com`
- stream name: `Production Website`

Record after creation:

- Analytics account name/ID;
- GA4 property name/ID;
- web stream name/ID;
- `G-...` measurement ID;
- administrators/editors with durable clinic control.

Do not place the measurement ID in production code until the privacy/measurement gate below is resolved.

## 4. Ownership model

GA4 must be a clinic-controlled business asset, not dependent on Behnam's unrelated analytics properties.

Preferred durable access:

- Dr. Farah / clinic retains administrator-level control;
- Behnam receives the level needed for implementation, audit and measurement operations;
- Windsor.ai/project analysis access is connected after property creation;
- access changes are documented as account administration rather than embedded in code.

## 5. Healthcare/privacy gate — supersedes the earlier site-wide-tag assumption

Earlier architecture assumed one site-wide Google tag footprint. Current official Google Analytics healthcare guidance requires a more conservative design for a US medical clinic.

Google states that Analytics customers must not send PII, and HIPAA-regulated entities must not expose Google to PHI. Google also states that authenticated pages are likely HIPAA-covered and that unauthenticated pages related to the provision of healthcare services may also be HIPAA-covered; customers should not place Google Analytics tags on HIPAA-covered pages.

Therefore:

1. **do not deploy GA4 site-wide by default;**
2. **do not tag booking/admin/authenticated pages unless specifically cleared;**
3. identify which public pages, if any, can lawfully/policy-compliantly use Google Analytics;
4. do not send names, email addresses, phone numbers, free-text symptoms, diagnosis, treatment, medication, test results or other patient/clinical details;
5. do not send sensitive health intent through page URLs, page titles, event names/parameters, custom dimensions, UTM parameters or form-interaction capture;
6. disable automatic measurement features that could capture unsafe context until each is reviewed;
7. align the privacy/cookie disclosure with the final implemented architecture.

This is both a compliance/policy boundary and a data-quality requirement.

## 6. Enhanced Measurement default

For the newly created stream, prefer **Enhanced Measurement OFF initially** until the implementation review is complete.

Reason: GA4 Enhanced Measurement can automatically collect page views and interaction types such as form interactions and site search. Those automatic events are useful on normal sites but are not an acceptable default on a healthcare website until we have confirmed what data each page/interaction can expose.

Individual measurement options can be enabled later where specifically justified and tested.

## 7. Production vs staging

Production measurement must not be polluted by staging traffic.

Target rule:

- production and staging must never share uncontrolled production analytics traffic;
- production tag inclusion must be explicit and hostname-aware;
- staging should no-op or use a dedicated test/debug arrangement;
- no production Ads/GA4 event should fire merely because the same static source is deployed to staging.

## 8. Tag architecture after privacy approval

For pages/events cleared for Google measurement, prefer the smallest repository-controlled implementation.

Initial engineering preference remains:

- direct Google tag / small analytics wrapper rather than GTM by default;
- no duplicate GA4 and Ads tag implementations;
- deterministic production/staging controls in code/deployment;
- GTM only if a concrete operational requirement later justifies it.

The exact destination relationship between the new GA4 stream and Google Ads tag `AW-17076731177` must be reviewed before deployment.

## 9. Measurement model

Keep the model compact and business-outcome oriented.

### Diagnostic events

Only on pages/interactions approved for Google measurement, examples may include:

- safe page/landing view;
- safe primary CTA interaction;
- click-to-call where policy/privacy design permits;
- technical/funnel diagnostics that contain no patient/health detail.

These are not automatically Ads primary conversions.

### Lead / secondary outcome

`booking_request_created`

Business meaning: a pending booking request was successfully created.

Do not send patient/clinical fields to GA4/Ads. If this event cannot be implemented without exposing PHI or linking a healthcare interaction impermissibly, keep the authoritative signal in first-party systems instead of forcing it into GA4.

### Primary business outcome

`visit_completed`

This remains the intended business optimization outcome, but its delivery to Google must use a compliant, minimal, deduplicated attribution design and may be better handled through a controlled first-party/offline conversion path rather than browser analytics.

Target business linkage:

`first-party acquisition/click context → booking attribution record → appointment → completed status → approved deduplicated outcome signal`

## 10. Attribution requirements

Preserve useful acquisition context in first-party systems where lawful/appropriate, including:

- first landing page;
- source / medium / campaign;
- relevant UTM values that do not contain PII or sensitive health information;
- partner/referral identifier;
- Google click identifiers such as GCLID where applicable and permitted;
- anonymous/internal marketing-session or attribution reference;
- booking/appointment linkage through opaque internal references.

Do not overload the legacy short `appointments.source` field with the entire attribution model.

## 11. Immediate next action

Owner action:

1. open Google Analytics under the clinic-controlled Google account;
2. create the production GA4 property using the specification in section 3;
3. create the production Web data stream;
4. leave tag installation for later;
5. preferably leave Enhanced Measurement off initially;
6. reconnect/authorize the GA4 property in Windsor.ai;
7. provide/verify the resulting property/stream/measurement IDs through the connected system.

After the property is visible to Windsor.ai, the project can capture the baseline and proceed to page/tag privacy classification and implementation design.

## 12. P2.2 completion evidence

P2.2 can be marked DONE when:

- new clinic-controlled GA4 property exists;
- durable ownership/access is confirmed;
- production web stream exists;
- property ID / stream ID / measurement ID are recorded;
- Windsor/project analysis access is connected;
- production/staging architecture is documented;
- healthcare/privacy tag boundary is documented;
- the relationship with Google Ads is understood;
- a controlled safe test event/pageview is validated **only after** the implementation/privacy gate permits deployment.

Tag/event implementation continues under P2.6–P2.11.