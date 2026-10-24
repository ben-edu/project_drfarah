# GA4 Discovery & Target Architecture — 2026-10-24

**Project:** Dr. Farah VIP Urgent Care  
**Roadmap item:** P2.2 Resolve GA4 access / property architecture  
**Status:** IN_PROGRESS — existing-property discovery before any new property is created

## 1. Verified current state

### FACT — Windsor.ai GA4 access

The Windsor.ai connection currently exposes only one GA4 property/account selection:

- property/account ID: `483894121`
- name: `safeguardsupport.com`

No Dr. Farah GA4 property is currently visible in the connected Windsor.ai workflow.

### FACT — Google Ads contains a legacy GA4-origin conversion action

The live Dr. Farah Google Ads account `652-510-3588` contains a hidden conversion action:

- name: `drfarahvipurgentcare.com (web) purchase`
- origin: `WEBSITE`
- type: `GOOGLE_ANALYTICS_4_PURCHASE`
- status: `HIDDEN`
- primary for goal: `False`
- no recorded last conversion date

This is evidence that a GA4-related website conversion was previously imported/configured in Google Ads. It does **not** by itself prove that the original GA4 property still exists, is correctly configured, is owned by the clinic, or is currently collecting data.

### FACT — repository measurement state

The current repository/source audit found no implemented Google tag, GTM container, GA4 event layer, or booking/call analytics in the inspected frontend source. The production assembly script does not currently inject analytics code.

Google Ads exposes site tag ID `AW-17076731177`, and Ads auto-tagging is enabled.

## 2. Immediate decision

**Do not create a new GA4 property yet.**

First attempt to discover and authorize any existing Dr. Farah GA4 property using the Google account that now has access to the clinic's Google assets. Creating a second property before discovery could fragment historical data, ownership, Ads links, and future reporting.

If no valid existing clinic-owned property can be found after authorization/account review, create a new clean production property under clinic-controlled ownership.

## 3. Existing-property acceptance criteria

An existing property is reusable only if all material conditions are satisfied:

1. it is for `drfarahvipurgentcare.com` / Dr. Farah VIP Urgent Care;
2. Dr. Farah / the clinic retains durable administrative control;
3. Behnam can receive the access level needed for implementation and analysis;
4. reporting timezone is or can be aligned to `America/Los_Angeles`;
5. currency is or can be aligned to USD;
6. the production web stream is identifiable and not materially contaminated by unrelated sites;
7. current or historical tag configuration can be understood;
8. Google Ads linkage/destinations can be reviewed and corrected;
9. no duplicate production measurement architecture would be created by reuse.

If these conditions fail materially, a new clinic-controlled production property may be cleaner than preserving a bad legacy implementation.

## 4. Target architecture

### 4.1 Ownership

GA4 should be a clinic-controlled business asset, not dependent on Behnam's unrelated personal/business analytics properties.

Preferred durable ownership model:

- clinic/Dr. Farah retains administrator-level control;
- Behnam receives the role needed to implement, audit, and manage measurement;
- access changes are documented as project/account administration, not embedded in code.

### 4.2 Production web stream

Target production site:

`https://drfarahvipurgentcare.com`

Target reporting timezone:

`America/Los_Angeles`

Target currency:

`USD`

The exact GA4 property ID, stream ID, and `G-...` measurement ID must be recorded only after the correct property/stream is verified.

### 4.3 Staging isolation

Production measurement must not be polluted by staging traffic.

Preferred initial approach for this static-site deployment:

- production receives the production Google tag;
- staging does not send events to the production GA4 property or Google Ads;
- event code may no-op or use explicit debug/test behavior outside the production hostname;
- a separate staging/test stream/property is optional later if repeated analytics QA justifies it.

This is simpler and safer than sending staging traffic into production and filtering it after collection.

### 4.4 One site-wide Google tag footprint

Use one site-wide Google tag implementation and connect the required Google destinations rather than installing independent duplicate tags for GA4 and Google Ads.

Initial target destinations:

- verified Dr. Farah GA4 web stream;
- Google Ads account/tag destination associated with `AW-17076731177`.

The exact destination/tag relationship must be reviewed after GA4 access is obtained, because Google Ads may already contain legacy tag/destination configuration.

### 4.5 Direct Google tag vs Google Tag Manager

**Initial recommendation:** direct Google tag + a small repository-controlled analytics wrapper, not GTM by default.

Reasons:

- current frontend is a controlled static site with normal Git/Jenkins deployment;
- required first-phase events are limited and known;
- production/staging behavior can be enforced in code/build controls;
- fewer moving parts reduces duplicate-tag and governance risk;
- custom business-outcome attribution (`visit_completed`) will depend primarily on first-party booking/admin linkage, not on a large browser-tag taxonomy.

Reconsider GTM later if there is a concrete need for frequent non-code tag changes, multiple third-party marketing tags, specialized experimentation, or delegated marketing operations that justify a container layer.

## 5. Measurement model

Keep browser/event measurement compact.

### Diagnostic / behavioral

Examples:

- page/landing view;
- primary CTA interaction;
- booking start;
- availability shown;
- click-to-call;
- technical booking failure where useful.

These events support funnel diagnosis and UX analysis. They should not automatically become Google Ads primary conversions.

### Lead / secondary outcome

`booking_request_created`

Trigger only after the booking API successfully creates the pending appointment. It is stronger than a button click but is not a completed visit.

### Primary business outcome

`visit_completed`

This is the intended optimization outcome once reliable attribution exists.

Target linkage:

`first-party acquisition/click context → booking attribution record → appointment → status=completed → deduplicated business-outcome conversion`

The completed-visit conversion should be generated from the authoritative booking/admin outcome rather than from a browser thank-you page.

## 6. Attribution requirements

Before paid relaunch, preserve enough first-party acquisition context to reconcile a booking and completed visit to marketing source where technically/policy appropriate, including:

- first landing page;
- source / medium / campaign;
- relevant UTM values;
- explicit partner/referral identifier;
- Google click identifiers such as GCLID and applicable equivalents when available and permitted;
- anonymous/internal marketing-session or attribution reference;
- booking/appointment linkage through an opaque internal reference.

Do not overload the legacy short `appointments.source` field with the entire attribution model.

## 7. Data-use boundary

Use useful lawful/platform-compliant measurement and optimization capabilities without unnecessary self-restriction.

Do not include unnecessary medical-record detail in GA4/Ads event payloads. In particular, do not send free-text symptoms, diagnoses, medications, treatment notes, test results, patient identifiers, or similarly unnecessary clinical content as analytics dimensions/events.

Service/intent information that could reveal sensitive health interests should be reviewed before being sent to Google advertising/analytics systems; internal first-party analytics may retain more business context where justified and governed.

The public privacy/cookie/tracking copy must be updated after the implemented stack is known so the disclosure matches actual behavior.

## 8. Immediate discovery action

Re-authorize/add Google Analytics 4 in Windsor.ai using the Google account that has access to Dr. Farah's Google assets, then inspect the property list.

Decision tree:

1. **Dr. Farah GA4 property appears** → connect it, inspect property/stream/ownership/history, and decide reuse vs cleanup.
2. **Property exists in Google Analytics but not under Behnam's account** → Dr. Farah grants suitable GA4 property access or authorizes the property through the clinic-controlled account.
3. **No Dr. Farah GA4 property exists** → create one clean clinic-controlled production property and web stream, then connect it.

Do not install a `G-...` ID on the site until the correct property/stream is verified.

## 9. P2.2 completion evidence

P2.2 can be marked DONE only when:

- correct clinic GA4 property is identified/created;
- durable ownership/access is confirmed;
- production web stream is identified;
- property ID / stream ID / measurement ID are recorded;
- production vs staging architecture is decided;
- Windsor/project analysis access is connected;
- Google Ads destination/link relationship is understood;
- a test pageview/event can be validated after implementation.

Implementation of the site tag/events continues under P2.6–P2.11.