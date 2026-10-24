# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.**  
> A new ChatGPT context/operator should be able to continue the project from this file + `ROADMAP.md` without reading old chats.

**Last updated:** 2026-10-24  
**Repository:** `ben-edu/project_drfarah`  
**Integration/default branch:** `dev`  
**Control-plane merge:** PR #78 merged to `dev` on 2026-10-24 — `c10b7bec5f9acad0531b88bac9056d4950d918a6`  
**Canonical roadmap:** `ROADMAP.md`  
**Single active ChatGPT project workspace:** existing `BG-20` tab, repurposed as the unified project workspace

---

## 1. Control-plane state

### Current decision

- GitHub is the durable project memory for roadmap, handoff, decisions, stable facts, code, runbooks and evidence.
- OpenProject remains authoritative for live work-package status, assignee, dates, dependencies, milestones and completion.
- Live systems remain authoritative for their own current state.
- The former specialized ChatGPT tab work is consolidated into the existing BG-20 tab and the master roadmap; old tabs are no longer needed for durable context once the Project Source replacement/resume test is complete.
- Separate workstream identities BG-00 through BG-90 remain valid for OpenProject mapping and handoffs.

### Current control-plane task

`P0.1` is **DONE**. PR #78 is merged to `dev` and the master roadmap/handoff/control documents are now on the default branch.

`P0.2` is **IN_PROGRESS**: replace the ChatGPT Project Source `.md` files with minimal routers that point only to `dev`.

Before deleting the other ChatGPT tabs, perform one quick resume test from the existing BG-20 tab:

1. read `PROJECT_HANDOFF.md` from `dev`;
2. read the current queue/relevant phase of `ROADMAP.md` from `dev`;
3. confirm the next task and blockers can be determined without old-tab context.

After that test succeeds, the old tabs may be retired without losing intended work.

---

## 2. Current strategic focus

Immediate project objective:

> stabilize booking + establish reliable marketing measurement + complete Google account baselines + correct high-confidence issues before paid relaunch.

The current high-level order is:

`Control plane → Booking health → GA4/Search Console access → Measurement/visit_completed → Google forensic baselines → High-confidence corrections → Economics/service priorities → Landing paths → Controlled Ads relaunch → Local/reputation cycle → Traveler/Pre-Op/Content → Growth Intelligence/scale`

This order is gate-based, not rigidly linear. Safe independent work may proceed around soft blockers.

---

## 3. Verified current facts

### Business

- Dr. Farah VIP Urgent Care
- 9229 Wilshire Blvd., Beverly Hills, CA 90210
- Phone: 310-467-0101
- Primary timezone: America/Los_Angeles / Pacific Time
- owner-confirmed regular hours currently recorded in project context: Monday–Friday 8:30 AM–5:30 PM; last patient before 5:00 PM.

### Repository / deployment

- repository: `ben-edu/project_drfarah`
- `dev` = integration/staging branch
- `main` = production branch
- Jenkins remains deployment authority
- current production/staging/deployment history remains in `HANDOFF.md`
- do not restart already accepted domain migration/deployment work because historical checklists remain in older docs.

### Booking / Brevo

`B-001` remains open.

The booking flow persists the appointment even if outbound email fails. Brevo-related delivery remediation is being handled in a separate technical workflow.

Paid traffic remains blocked until a controlled production booking verifies the expected notification behavior.

### Website measurement

Repository/source audit found no implemented Google tag/GTM/GA4 event layer or booking/call analytics in inspected site source, and production assembly did not inject one.

Google Ads live account exposes Google tag:

`AW-17076731177`

Google Ads auto-tagging is enabled.

The project must still verify production runtime before claiming no third-party tag is present outside Git.

The current website privacy copy states essential-cookie/no-third-party-tracking behavior; this must be updated after the final measurement/consent architecture is implemented so public copy matches reality.

### Canonical conversion direction

Use a compact model:

- diagnostic funnel events for debugging/UX;
- `booking_request_created` as a lead/secondary signal after successful booking API creation;
- `visit_completed` as the intended primary business outcome once reliable appointment/source linkage and Ads import are validated.

Do not mislabel a pending booking request as a completed patient visit.

### Google Ads access and historical reality

Windsor.ai connection is operational for Dr. Farah Google Ads account:

- Customer ID: `652-510-3588`
- currency: USD
- timezone: America/Los_Angeles
- status: enabled
- no manager/MCC account on the customer
- auto-tagging: enabled
- conversion tracking managed by self

The prior assumption that no campaign ever ran is **superseded**.

Verified historical campaign:

- `Urgent Care Medical Center`
- type: Smart
- current status: paused
- activity: June 2025 through February 2026
- impressions: 258,541
- clicks: 5,590
- spend: $4,494.8619
- platform-reported conversions: 16
- platform conversion cost: roughly $281 per reported conversion, but business outcome quality is not yet reconciled.

Known current conversion actions include Google-hosted/call/map actions and a hidden GA4 purchase action. Current primary goals are not yet aligned to `visit_completed`.

Detailed baseline: `docs/GOOGLE_ADS_BASELINE_2026-10-24.md`.

### Google Business Profile access and baseline

Windsor.ai connection is operational for the live profile:

- title: Dr Farah VIP Urgent Care
- status: open
- primary category: Urgent care center
- website: https://drfarahvipurgentcare.com/
- phone: (310) 467-0101
- address: 9229 Wilshire Blvd, Beverly Hills, CA 90210
- Voice of Merchant: true
- all-time rating at last check: 5.0
- all-time review count at last check: 109

Recent 90-day profile performance at last query:

- impressions: 3,860
- website clicks: 130
- call clicks: 120
- direction requests: 205

Current live regular hours show Friday closing at 16:30 while owner-confirmed project hours were 17:30. Verify current clinic truth immediately before changing the profile.

The service catalogue is extensive. **Do not bulk-delete services merely because the list is long.** Evaluate actual availability, demand, economics, clarity, duplication, claims/pricing accuracy, conversion usefulness and Google policy before changing service entries.

Detailed baseline: `docs/GBP_BASELINE_2026-10-24.md`.

### GA4 / Search Console

Dr. Farah production GA4 and Search Console sources are not yet connected/verified in the current project data workflow.

This is a current priority, not a future optional task.

---

## 4. Current blockers

### B-001 — Booking/Brevo delivery

**State:** IN_PROGRESS  
**Class:** HARD for paid launch / SOFT for read-only research  
**Unblock evidence:** controlled production booking persists and expected notification/receipt behavior is verified.  
**Safe parallel:** Ads/GBP/SC/GA4 work, measurement design, research, economics baselines.

### B-002 — Measurement implementation not yet live

**State:** IN_PROGRESS  
**Class:** HARD for paid relaunch  
**Established:** source audit + Ads tag availability.  
**Still needed:** runtime validation, GA4 property/data stream, source/GCLID persistence, conversion architecture, `visit_completed` linkage/import, privacy/cookie alignment, end-to-end validation.

### B-003 — GA4 production access/property unresolved

**State:** READY  
**Class:** HARD for full measurement baseline / SOFT for Ads/GBP forensic work  
**Unblock evidence:** correct Dr. Farah property/data stream identified/connected and test data observed.

### B-004 — Search Console production access/property unresolved

**State:** READY  
**Class:** HARD for BG30-04 / SOFT for Ads/GBP work  
**Unblock evidence:** correct `drfarahvipurgentcare.com` property verified/connected; sitemap/indexing data readable.

### B-005 — Project Source replacement / resume test pending

**State:** IN_PROGRESS  
**Class:** HARD only for retiring old ChatGPT tabs / SOFT for all repository and live-system work  
**Established:** PR #78 is merged and core control files are present on `dev`.  
**Unblock evidence:** minimal Project Source routers uploaded and a resume test confirms the BG-20 workspace can determine current state/next action from `dev` without old tabs.

---

## 5. Work completed in the current control/marketing effort

- unified project-control PR #78 created and squash-merged to `dev` on 2026-10-24 (`c10b7bec5f9acad0531b88bac9056d4950d918a6`);
- `ROADMAP.md` converted into one master roadmap and expanded to preserve former-tab work;
- full known OpenProject maps for BG-00, BG-20, BG-30, BG-40, BG-50, BG-60 and BG-80 preserved in the roadmap;
- known BG70/BG90 identifiers preserved without fabricating unknown IDs;
- website/booking/deployment obligations integrated into the master roadmap rather than treated as a second roadmap;
- `docs/PROJECT_OPERATING_MODEL.md` created;
- `docs/BUSINESS_GROWTH_SOURCE.md` created;
- `docs/MEASUREMENT_BASELINE_2026-10-21.md` created;
- `docs/CONVERSION_MEASUREMENT_SPEC.md` created;
- live Google Ads baseline captured;
- live GBP baseline captured;
- prior “no Ads history” assumption disproven and replaced with live evidence;
- Google Ads/GBP Windsor connections verified.

---

## 6. Exact next actions

Follow this order unless a hard blocker forces a bypass.

### Next A — finish Project Source migration and prove resume continuity

1. replace the uploaded Project Sources with the final minimal routers that point only to `dev`;
2. from the BG-20 workspace, read `PROJECT_HANDOFF.md` + the relevant `ROADMAP.md` phase from `dev`;
3. confirm the workspace can identify B-001 through B-005 and the next eligible task without old-tab context;
4. mark B-005 resolved;
5. old specialized ChatGPT tabs may then be retired at the owner's discretion.

### Next B — resolve GA4

1. identify existing Dr. Farah GA4 property/data stream or create/authorize the correct one through the approved account workflow;
2. connect it to the project/Windsor workflow where supported;
3. preserve staging/production separation;
4. record property/data-stream details safely;
5. validate event receipt after implementation.

### Next C — resolve Search Console

1. identify/verify production property;
2. authorize project access;
3. confirm sitemap/indexing visibility;
4. capture BG30-04 baseline.

### Next D — finish measurement architecture and implementation

1. runtime tag check;
2. Google tag / GA4 implementation;
3. source/UTM/GCLID persistence;
4. `booking_request_created` event;
5. `visit_completed` linkage/import design + implementation;
6. call/lead tracking as useful;
7. privacy/cookie copy update after actual implementation is known;
8. end-to-end controlled validation.

### Next E — continue Google forensic audits in parallel

Ads:

- historical monthly/campaign audit;
- conversion-action quality;
- search terms/intent where available;
- geo/device/day-hour;
- rules/assets/landing destinations;
- reconcile platform conversions to actual business outcomes if records allow.

GBP:

- complete profile/service/category/review/search-keyword baseline;
- verify Friday hours before correction;
- assess service catalogue strategically, not by arbitrary count;
- prepare high-confidence corrections only after before-state is preserved.

---

## 7. Do not do yet

- do not launch or materially scale paid Google Ads while G1/G2 are red;
- do not optimize Ads toward low-quality Google-hosted actions as if they equal completed patients;
- do not bulk-delete GBP services because the catalogue is large;
- do not create a second roadmap for website, marketing or Growth Intelligence;
- do not invent unknown OpenProject identifiers;
- do not publish mobile/24-hour/emergency/insurance/referral claims without current operational/compliance support;
- do not send unnecessary clinical record detail to analytics/ad platforms;
- do not leave a material new fact only in chat.

---

## 8. Safe parallel work

If Brevo/GA4/Search Console causes waiting, continue the highest-value independent item among:

- Google Ads forensic audit;
- GBP/review/local visibility analysis;
- competitor/query research;
- source taxonomy;
- service/revenue baseline request;
- BG70 service priority framework;
- traveler baseline reconstruction;
- pre-op baseline/economics reconstruction;
- content research based on verified patient/search questions.

Re-check blocked higher-priority items at the next session before starting new lower-priority work.

---

## 9. OpenProject continuity

OpenProject remains the execution/status authority.

The master roadmap preserves the workstreams, but it does **not** overwrite live OpenProject status.

When a roadmap action reaches a material execution state change, update the corresponding OpenProject work package separately when access/evidence is available.

Do not infer `DONE` in OpenProject from a GitHub recommendation alone.

---

## 10. Resume instructions for any future context

Read:

1. `README.md`;
2. this file;
3. `ROADMAP.md` current priority queue + relevant phase;
4. `docs/DECISIONS.md` if the task involves approval/strategy;
5. relevant dated baseline/spec/runbook;
6. live system if current state could have changed.

Then:

1. re-check B-001 through B-005;
2. select the highest-priority READY task without an unsatisfied HARD dependency;
3. execute and validate;
4. update this handoff before ending the material session.

Do not require old ChatGPT tabs or prior chat context to continue the project.
