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

`P0.2` final minimal Project Sources: **owner configuration task; not a blocker for execution**.

---

## 2. Current strategic focus

Immediate objective:

> validate the merged first-party attribution foundation, build a privacy-safe `visit_completed` business-outcome read model, keep Google measurement blocked until eligible pages/events are approved, then build controlled Ads offline conversion import and prepare a measured paid relaunch.

Current order:

`first-party attribution validation → visit_completed → GA4/privacy page classification → approved minimal Google tag if permitted → Ads offline conversion import → Search/Ads/GBP forensic baselines and corrections → economics/service priorities → landing paths → controlled Ads relaunch → local/reputation cycle → Traveler/Pre-Op/Content → Growth Intelligence/scale`

The roadmap is gate-based, not rigidly linear. If a HARD dependency blocks one item, record the restart condition and continue the highest-value independent READY item.

---

## 3. Verified current facts

### Booking / Brevo

**OWNER-CONFIRMED FACT:** website email/Brevo issue is resolved.

- prior blocker B-001 is CLOSED;
- `P1.1` should be treated as DONE;
- `G1-BOOKING-HEALTHY` is GREEN unless new regression evidence appears;
- Brevo is not the reason paid relaunch is blocked.

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

Detailed baseline: `docs/GOOGLE_ADS_BASELINE_2026-10-24.md`.

### Google Business Profile

Live profile access is operational. Latest captured baseline:

- Dr Farah VIP Urgent Care
- 5.0 rating / 109 reviews at capture
- primary category: Urgent care center
- correct website/phone/address captured

Do not bulk-delete services because the catalogue is large. Change services only for clear factual, strategic, demand, economics, clarity, duplication, claims/pricing, UX or policy reasons.

Detailed baseline: `docs/GBP_BASELINE_2026-10-24.md`.

### GA4 — access and production stream metadata resolved

**FACT — verified 2026-10-26:** Windsor.ai exposes the correct clinic GA4 property:

- property ID: `489069776`
- name: `drfarahvipurgentcare.com`

**OWNER-PROVIDED GA4 ADMIN METADATA — 2026-10-26:**

- Web Stream ID: `11211773871`
- Measurement ID: `G-D58FTMF05S`

A live recent-period data query succeeds and returns zero rows/events, which is consistent with the fact that no approved production GA4 tag/event implementation is currently active on the site.

The unrelated property `483894121` (`safeguardsupport.com`) is not part of this project.

Still needed:

- timezone/currency/Enhanced Measurement live-setting confirmation;
- appropriate legal/privacy classification of any pages/events proposed for Google measurement;
- Google Ads link/destination review;
- controlled first event only after tag deployment is approved.

Current Google Analytics guidance for HIPAA-regulated entities says Google Analytics must not receive PHI and does not offer a HIPAA BAA; authenticated pages are likely HIPAA-covered and some unauthenticated healthcare-service pages may also need exclusion. Do not deploy GA4 site-wide by default.

Detailed architecture: `docs/GA4_ARCHITECTURE_2026-10-24.md`.

### Search Console — access resolved

**FACT — verified 2026-10-26:** the correct domain property is connected and readable:

`sc-domain:drfarahvipurgentcare.com`

90-day Search Analytics baseline through 2026-10-24:

- 314 clicks
- 33,135 impressions
- 0.95% CTR
- average position 11.76

Important early signals:

- exact brand query performs strongly;
- local non-brand urgent-care queries have meaningful impressions but weaker position/CTR;
- educational wound-care content drives substantial organic visibility;
- HTTP homepage variant still appears in historical Search Console data and requires current redirect/canonical verification before treating it as an active defect.

The sitemap contradiction was corrected on 2026-10-26: `/book` and `/patient-registration` remain `noindex` and are no longer listed in the XML sitemap.

Detailed baseline: `docs/SEARCH_CONSOLE_BASELINE_2026-10-26.md`.

### Measurement direction

Compact model:

- diagnostic signals only where they answer a real question;
- `booking_request_created` = secondary lead signal;
- `visit_completed` = intended primary business outcome.

Do not equate platform conversions with completed patient visits.

### First-party attribution implementation

**MERGED TO `dev` 2026-10-26 after owner-confirmed successful Jenkins validation.**

Merged PR: `#83` / merge commit `799c0a021c8b2c1067570205f13555b71761415b`.

Implementation scope:

- capture canonical source + UTM values + GCLID/GBRAID/WBRAID + explicit partner/traveler marker + opaque marketing session ID;
- preserve first-touch and useful last-touch context;
- session storage for current-session continuity;
- persistent first-party attribution only after site preference acceptance;
- no page path, service, reason-for-visit, PII or clinical data in the marketing attribution record;
- structured 1:1 `appointment_attributions` table linked to appointment;
- retain compact legacy `appointments.source` for compatibility;
- migration revision `0004` with fail-closed bootstrap coverage;
- booking POST persists attribution atomically with appointment;
- privacy page and cookie notice updated to match first-party attribution behavior;
- no GA4/Ads tag deployed by this implementation.

Staging behavior still needs an end-to-end campaign-marker persistence check after the merged `dev` build is available.

### `visit_completed` business outcome

**IN PROGRESS on branch:** `feature/visit-completed-read-model-20261026`

Initial design deliberately uses a read model rather than another event table:

- authoritative condition: `Appointment.status == completed`;
- one deterministic outcome key per appointment: `visit_completed:<appointment_id>`;
- stable initial occurrence time: appointment `starts_at`;
- join non-clinical acquisition identifiers from `appointment_attributions`;
- no patient name, email, phone, reason-for-visit, service/clinical context or registration data in the marketing outcome row;
- no external transmission yet.

Detailed contract: `docs/VISIT_COMPLETED_OUTCOME_2026-10-26.md`.

---

## 4. Current blockers / dependencies

### B-001 — Booking/Brevo

**State:** RESOLVED / CLOSED.

### B-002 — Measurement implementation not yet production-ready

**State:** IN_PROGRESS  
**Class:** HARD for paid relaunch

Still needed:

- staging validation of merged first-party attribution;
- `visit_completed` read-model CI + staging validation;
- appropriate healthcare/privacy page/event classification before any Google tag deployment;
- controlled Google tag/consent implementation only where permitted;
- `booking_request_created` policy/implementation decision;
- Ads offline conversion import design and deduplication validation;
- end-to-end no-duplicate/no-sensitive-data validation.

### B-003 — GA4 access / stream metadata

**State:** RESOLVED / TAG DEPLOYMENT GATED  
**Class:** no longer an access or ID blocker.

Property `489069776`, Web Stream ID `11211773871`, and Measurement ID `G-D58FTMF05S` are recorded. Remaining work is privacy/page eligibility + live setting confirmation + controlled implementation.

### B-004 — Search Console access

**State:** ACCESS RESOLVED / TECHNICAL BASELINE CONTINUES  
**Class:** no longer an access blocker.

Search Analytics is readable. Sitemap contradiction has been corrected; current indexing/canonical/redirect coverage still needs dedicated validation.

### B-005 — Project Source cleanup

**State:** owner configuration task; not an execution blocker.

---

## 5. Exact next actions

1. run repository CI/Jenkins for branch `feature/visit-completed-read-model-20261026` and merge only if clean;
2. validate merged first-party attribution on staging: campaign marker survives navigation to booking and persists to `appointment_attributions` without clinical data;
3. validate `visit_completed` read model against staged completed/non-completed appointments;
4. inspect Google Ads offline-conversion capabilities and exact deduplication/import fields;
5. define the approved completed-visit conversion action and controlled import path without PII/PHI;
6. separately obtain the appropriate legal/privacy classification for any pages proposed for GA4 measurement;
7. only if approved, implement a production-only page allowlist + basic consent loader for `G-D58FTMF05S`;
8. complete Search Console indexing/canonical technical baseline and continue Ads/GBP forensic corrections in parallel;
9. keep `G2-MEASUREMENT-READY` red until the controlled source → appointment → completed visit → import test passes.

---

## 6. Do not do yet

- do not relaunch/materially scale Google Ads while `G2-MEASUREMENT-READY` is red;
- do not deploy GA4 site-wide by default on the healthcare site;
- do not tag booking, patient-registration, admin or authenticated flows by default;
- do not send unnecessary PII/PHI, service/clinical context or health intent to Google analytics/advertising systems;
- do not make page views, directions or generic call clicks the long-term primary Ads outcome;
- do not upload `visit_completed` rows to Google until the Ads conversion action/import contract and deduplication behavior are validated;
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
