# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** A new ChatGPT context/operator must be able to continue from this file + `ROADMAP.md` without reading old chats or deleted project tabs.

**Last updated:** 2026-10-26  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Canonical roadmap:** `ROADMAP.md`  
**Single active ChatGPT project workspace:** this conversation, historically named `BG-20`

---

## 1. Control plane

- GitHub is durable project memory for roadmap, handoff, decisions, code, runbooks, evidence and accepted implementation state.
- `ROADMAP.md` is the only master sequencing document.
- OpenProject remains authoritative for live work-package state, assignee, dates, dependencies, milestones and completion.
- Live systems are authoritative for their own current state.
- Former BG-00 through BG-90 chat tabs are logical workstreams only; they are not required for continuity.
- Project Source `.md` files are bootstrap/router files only and must not become a second project database.

`P0.1` unified control plane on `dev`: **DONE**.

---

## 2. Current strategic focus

Immediate objective:

> validate selected-page GA4 production measurement, validate first-party attribution + `visit_completed` end to end, then build a controlled Google Ads completed-visit import and continue forensic Ads/GBP/Search work toward a measured paid relaunch.

Current order:

`first-party attribution validation → selected-page GA4 validation → visit_completed validation → Ads offline completed-visit import → Search/Ads/GBP forensic baselines and corrections → economics/service priorities → landing paths → controlled Ads relaunch → local/reputation cycle → Traveler/Pre-Op/Content → Growth Intelligence/scale`

The roadmap is gate-based, not rigidly linear. If a HARD dependency blocks one item, record the restart condition and continue the highest-value independent READY item.

---

## 3. Verified current facts

### Booking / Brevo

**OWNER-CONFIRMED FACT:** website email/Brevo issue is resolved.

- prior blocker B-001 is CLOSED;
- `P1.1` is DONE;
- `G1-BOOKING-HEALTHY` is GREEN unless new regression evidence appears.

### Google Ads

Windsor.ai access is operational for account `652-510-3588`.

Historical campaign evidence supersedes the old zero-history assumption:

- `Urgent Care Medical Center`
- Smart campaign, paused
- activity June 2025–February 2026
- 258,541 impressions
- 5,590 clicks
- $4,494.8619 spend
- 16 platform-reported conversions

Google Ads tag destination: `AW-17076731177`. Auto-tagging is enabled.

Windsor's current Google Ads write-action set does **not** include offline click-conversion upload. `visit_completed` import therefore needs another controlled mechanism such as Google Ads API/Data Manager or another supported import path.

Detailed baseline: `docs/GOOGLE_ADS_BASELINE_2026-10-24.md`.

### Google Business Profile

Live profile access is operational. Latest captured baseline:

- Dr Farah VIP Urgent Care
- 5.0 rating / 109 reviews at capture
- primary category: Urgent care center
- correct website/phone/address captured

Do not bulk-delete services because the catalogue is large. Change services only for clear factual, strategic, demand, economics, clarity, duplication, claims/pricing, UX or policy reasons.

Detailed baseline: `docs/GBP_BASELINE_2026-10-24.md`.

### GA4 — access and stream metadata resolved

**FACT — verified 2026-10-26:**

- property ID: `489069776`
- property name: `drfarahvipurgentcare.com`
- Web Stream ID: `11211773871`
- Measurement ID: `G-D58FTMF05S`
- Windsor.ai access works.

Unrelated property `483894121` (`safeguardsupport.com`) is not part of this project.

### Search Console — access resolved

Correct domain property:

`sc-domain:drfarahvipurgentcare.com`

90-day Search Analytics baseline through 2026-10-24:

- 314 clicks
- 33,135 impressions
- 0.95% CTR
- average position 11.76

Sitemap contradiction corrected on 2026-10-26: `/book` and `/patient-registration` remain `noindex` and are no longer listed in XML sitemap.

Detailed baseline: `docs/SEARCH_CONSOLE_BASELINE_2026-10-26.md`.

### First-party attribution

**MERGED TO `dev` 2026-10-26 after owner-confirmed Jenkins success.**

PR #83 / merge commit `799c0a021c8b2c1067570205f13555b71761415b`.

Implemented:

- canonical source + UTM values + GCLID/GBRAID/WBRAID;
- partner/traveler marker;
- opaque marketing session ID;
- first-touch and useful last-touch context;
- session continuity plus optional persistent first-party storage;
- structured `appointment_attributions` record linked 1:1 to appointment;
- no page path, service, reason-for-visit, PII or clinical data in attribution record;
- migration revision `0004` with fail-closed bootstrap coverage;
- booking POST persists attribution atomically.

Still required: staging end-to-end validation after current `dev` build is available.

### `visit_completed`

**MERGED TO `dev` 2026-10-26 after owner-confirmed Jenkins success.**

PR #86 / merge commit `e5e87aa99cb23efd36159355e7597c4e30c5b65e`.

Contract:

- authoritative condition: `Appointment.status == completed`;
- deterministic key: `visit_completed:<appointment_id>`;
- stable occurrence time: appointment `starts_at`;
- joins non-clinical source/click attribution only;
- excludes patient name, email, phone, reason, service/clinical context and registration data;
- no external upload yet.

Detailed contract: `docs/VISIT_COMPLETED_OUTCOME_2026-10-26.md`.

### Selected-page GA4 production implementation

**IN VALIDATION on branch:** `feature/ga4-public-measurement-20261026`

Implementation:

- `frontend/analytics.js` uses Measurement ID `G-D58FTMF05S`;
- Google tag is injected only during production assembly, not staging source HTML;
- production allowlist: `/about`, `/contact`, `/privacy`, `/terms`, `/accessibility`, `/notice-of-privacy-practices`;
- runtime wrapper independently verifies production hostname + allowlist;
- homepage, booking, registration, services, treatment/condition pages and authenticated/admin flows are excluded;
- Consent Mode defaults analytics/ad storage to denied; analytics storage becomes granted only after explicit acceptance;
- limited cookieless consent-mode measurement can occur on allowlisted pages while analytics storage is denied;
- `ad_storage`, `ad_user_data`, and `ad_personalization` remain denied;
- automatic page views are suppressed; only a controlled manual page classification is sent;
- query strings, document title, detailed referrer and patient/clinical/form data are not intentionally sent;
- privacy notice is updated to match the implementation;
- production assembly has fail-closed checks preventing known excluded pages from receiving the Google wrapper.

Detailed architecture: `docs/GA4_ARCHITECTURE_2026-10-24.md`.

---

## 4. Current blockers / dependencies

### B-001 — Booking/Brevo

**State:** RESOLVED / CLOSED.

### B-002 — Measurement end-to-end validation

**State:** IN_PROGRESS  
**Class:** HARD for paid relaunch

Still needed:

- Jenkins validation of `feature/ga4-public-measurement-20261026`;
- staging validation of first-party source/click persistence to `appointment_attributions`;
- post-deploy validation that GA4 loads only on allowlisted production pages;
- GA4 Realtime/DebugView confirmation of one controlled safe page view;
- confirm GA4 timezone/currency/Enhanced Measurement settings;
- design and validate Google Ads `visit_completed` offline import with deduplication;
- end-to-end source → appointment → completed visit → import validation.

### B-003 — GA4 access / IDs

**State:** RESOLVED.  
No longer a blocker.

### B-004 — Search Console access

**State:** ACCESS RESOLVED / TECHNICAL BASELINE CONTINUES.

### B-005 — Project Source cleanup

**State:** owner configuration task; not an execution blocker.

---

## 5. Exact next actions

1. run Jenkins for `feature/ga4-public-measurement-20261026`;
2. if clean, merge the GA4 implementation PR to `dev`;
3. deploy through normal Jenkins/staging/production controls;
4. verify excluded pages make no Google measurement requests and allowlisted pages use the expected Consent Mode behavior;
5. confirm one controlled GA4 page view in Realtime/DebugView;
6. validate first-party campaign-marker persistence through booking into `appointment_attributions`;
7. validate completed/non-completed appointment behavior in `visit_completed`;
8. design the Google Ads offline completed-visit conversion action/import contract using click IDs and deduplication, without patient/clinical payload;
9. continue Search Console indexing/canonical work and Ads/GBP forensic corrections in parallel;
10. keep `G2-MEASUREMENT-READY` red until the controlled end-to-end source → completed visit → Ads import test passes.

---

## 6. Do not do yet

- do not relaunch/materially scale Google Ads while `G2-MEASUREMENT-READY` is red;
- do not tag booking, patient-registration, admin/authenticated or treatment/condition pages with Google Analytics under the current configuration;
- do not send unnecessary PII/PHI or clinical intent into analytics/advertising systems;
- do not make page views, directions or generic call clicks the long-term primary Ads outcome;
- do not upload `visit_completed` until the Google Ads conversion action/import and dedup behavior are validated;
- do not bulk-delete GBP services merely because the list is long;
- do not create another roadmap or depend on deleted chat tabs;
- do not leave material project results only in chat.

---

## 7. Resume protocol

Read in order:

1. `README.md` on `dev`;
2. this `PROJECT_HANDOFF.md`;
3. `ROADMAP.md` current priority queue + relevant phase;
4. `docs/DECISIONS.md` when approval/strategy matters;
5. relevant dated baseline/spec/runbook/code only as needed;
6. live system when current state may have changed;
7. OpenProject when live work-package metadata matters.

Then re-check blockers, select the highest-priority eligible task, execute/validate, record evidence, and update this handoff before ending material work.
