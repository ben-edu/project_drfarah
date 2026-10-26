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

> complete the first-party measurement/attribution foundation, then activate only approved Google measurement, build `visit_completed`, finish Google forensic baselines/corrections, and prepare a controlled paid relaunch optimized toward real business outcomes.

Current order:

`first-party attribution → GA4 stream/tag/privacy implementation → visit_completed → Search/Ads/GBP forensic baselines and corrections → economics/service priorities → landing paths → controlled Ads relaunch → local/reputation cycle → Traveler/Pre-Op/Content → Growth Intelligence/scale`

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

### GA4 — access now resolved

**FACT — verified 2026-10-26:** Windsor.ai now exposes the correct clinic GA4 property:

- property ID: `489069776`
- name: `drfarahvipurgentcare.com`

A live recent-period data query succeeds and returns zero rows/events, which is consistent with the fact that no approved production GA4 tag/event implementation is currently active on the site.

The unrelated property `483894121` (`safeguardsupport.com`) is not part of this project.

Still needed:

- exact production Web stream ID;
- exact `G-...` measurement ID;
- timezone/currency/Enhanced Measurement live-setting confirmation;
- approved page/event boundary;
- Google Ads link/destination review;
- controlled first event after implementation.

Detailed architecture: `docs/GA4_ARCHITECTURE_2026-10-24.md`.

### Search Console — access now resolved

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
- HTTP homepage variant still appears in historical Search Console data and requires canonical/redirect verification before treating it as a current defect.

Detailed baseline: `docs/SEARCH_CONSOLE_BASELINE_2026-10-26.md`.

### Measurement direction

Compact model:

- diagnostic signals only where they answer a real question;
- `booking_request_created` = secondary lead signal;
- `visit_completed` = intended primary business outcome once source-to-appointment linkage/import is validated.

Do not equate platform conversions with completed patient visits.

### First-party attribution implementation

**IN PROGRESS on branch:** `feature/attribution-foundation-20261026`

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

This foundation is designed so `visit_completed` can later join the authoritative appointment outcome to acquisition identifiers without depending on browser analytics.

---

## 4. Current blockers / dependencies

### B-001 — Booking/Brevo

**State:** RESOLVED / CLOSED.

### B-002 — Measurement implementation not yet production-ready

**State:** IN_PROGRESS  
**Class:** HARD for paid relaunch

Still needed after attribution foundation:

- GA4 stream/measurement metadata;
- approved healthcare/privacy page/event classification;
- controlled Google tag/consent implementation where permitted;
- `booking_request_created` validation;
- `visit_completed` outcome generation/import;
- end-to-end no-duplicate/no-sensitive-data validation.

### B-003 — GA4 access

**State:** ACCESS RESOLVED / IMPLEMENTATION PENDING  
**Class:** no longer an access blocker.

Property `489069776` is connected. Remaining work is implementation metadata + approved event/tag architecture.

### B-004 — Search Console access

**State:** ACCESS RESOLVED / TECHNICAL BASELINE CONTINUES  
**Class:** no longer an access blocker.

Search Analytics is readable. Sitemap/indexing/canonical coverage still needs dedicated validation.

### B-005 — Project Source cleanup

**State:** owner configuration task; not an execution blocker.

---

## 5. Exact next actions

1. validate branch `feature/attribution-foundation-20261026` with repository CI/tests and merge only if clean;
2. validate first-party attribution on staging: campaign marker survives navigation to booking and persists to the appointment attribution record;
3. obtain/record GA4 Web stream ID + `G-...` measurement ID and confirm timezone/currency/Enhanced Measurement settings;
4. classify which pages/events are eligible for Google measurement and implement the smallest compliant production-only Google tag footprint;
5. implement `visit_completed` generation/import from authoritative appointment completion with deduplication;
6. complete Search Console sitemap/indexing/canonical technical baseline;
7. continue Google Ads historical forensic audit and GBP high-confidence corrections in parallel where safe;
8. keep `G2-MEASUREMENT-READY` red until the controlled end-to-end test passes.

---

## 6. Do not do yet

- do not relaunch/materially scale Google Ads while `G2-MEASUREMENT-READY` is red;
- do not deploy GA4 site-wide by default on the healthcare site without page/event classification;
- do not tag booking/admin/authenticated flows by default;
- do not send unnecessary PII/PHI or clinical intent to Google analytics/advertising systems;
- do not make page views, directions or generic call clicks the long-term primary Ads outcome;
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
