# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** A new ChatGPT context/operator must be able to continue from this file + `ROADMAP.md` without reading old chats or deleted project tabs.

**Last updated:** 2026-10-24  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Canonical roadmap:** `ROADMAP.md`  
**Single active ChatGPT project workspace:** this conversation, historically named `BG-20`  

---

## 1. Control-plane state

- GitHub is the durable project memory for roadmap, handoff, decisions, stable facts, code, runbooks and evidence.
- `ROADMAP.md` is the only master sequencing document.
- OpenProject remains authoritative for live work-package status, assignee, dates, dependencies, milestones and completion.
- Live systems remain authoritative for their own current state.
- Separate ChatGPT workstream tabs are no longer required. Their intended work is preserved in `ROADMAP.md` under BG-00 through BG-90.
- The Project Source `.md` files are bootstrap/router files only. They must not become a second source of project truth.

### Current control-plane task

`P0.1` — unified control plane on `dev`: **DONE**.

`P0.2` — replace Project Sources with final minimal single-workspace routers: **IN_PROGRESS / owner action**.

`P0.3` — retire/delete old specialized ChatGPT tabs: **READY**. The project is designed to continue without them. After the owner replaces the Project Sources, this current conversation can remain as the only project tab.

---

## 2. Current strategic focus

Immediate objective:

> complete GA4/Search Console access and the measurement/privacy/attribution foundation; finish Google forensic baselines and high-confidence corrections; then prepare a controlled Ads relaunch optimized toward real business outcomes.

Current high-level order:

`Project Source replacement → GA4 + Search Console → measurement/privacy + visit_completed → Ads/GBP/Search baselines → high-confidence corrections → economics/service priorities → landing paths → controlled Ads relaunch → local/reputation cycle → Traveler/Pre-Op/Content → Growth Intelligence/scale`

The roadmap is gate-based, not rigidly linear. If a task is blocked, preserve the blocker/restart condition and continue the highest-value independent READY task.

---

## 3. Verified current facts

### Booking / Brevo email service

**OWNER-CONFIRMED FACT — 2026-10-24:** the website email service / Brevo problem has been resolved.

Treat the prior Brevo incident as **DONE** unless new production evidence shows a regression.

Accordingly:

- former blocker `B-001` is closed;
- `P1.1` should be treated as DONE;
- `G1-BOOKING-HEALTHY` is currently considered GREEN based on owner confirmation;
- Brevo is no longer a blocker for measurement implementation or future paid launch.

Paid launch is still blocked by the measurement/attribution gate, not by Brevo.

### Repository / deployment

- repository: `ben-edu/project_drfarah`
- `dev` = integration/staging branch
- `main` = production branch
- Jenkins remains deployment authority
- detailed historical production/deployment evidence remains in `HANDOFF.md`
- do not restart completed domain/deployment work because older checklists remain in historical files.

### Website measurement

Repository/source audit found no implemented Google tag/GTM/GA4 event layer or booking/call analytics in the inspected site source and production assembly did not inject one.

Google Ads exposes Google tag:

`AW-17076731177`

Google Ads auto-tagging is enabled.

Runtime validation and implementation are still required.

The current website privacy/tracking copy must be updated after the actual measurement/consent architecture is implemented so public disclosures match reality.

### Conversion direction

Use a compact model:

- diagnostic events for funnel/technical analysis;
- `booking_request_created` as a lead/secondary signal;
- `visit_completed` as the intended primary business-outcome conversion once source/appointment linkage and Ads import are validated.

Do not optimize long-term toward superficial platform actions when completed-visit data is available.

### Google Ads

Windsor.ai access is operational for Dr. Farah Google Ads account `652-510-3588`.

The former assumption that no campaign ever ran is superseded.

Verified historical campaign:

- `Urgent Care Medical Center`
- type: Smart
- status: paused
- activity: June 2025 through February 2026
- impressions: 258,541
- clicks: 5,590
- spend: $4,494.8619
- platform-reported conversions: 16

Detailed baseline: `docs/GOOGLE_ADS_BASELINE_2026-10-24.md`.

BG20-01 is a **historical forensic audit + relaunch-readiness audit**.

### Google Business Profile

Windsor.ai access is operational for the live profile.

Latest captured baseline included:

- title: Dr Farah VIP Urgent Care
- primary category: Urgent care center
- rating: 5.0
- total reviews: 109
- website: https://drfarahvipurgentcare.com/
- phone: (310) 467-0101
- address: 9229 Wilshire Blvd, Beverly Hills, CA 90210

The service catalogue is extensive. Do not delete services merely because the list is long. Evaluate actual availability, demand, economics, clarity, duplication, claims/pricing accuracy, conversion usefulness and Google policy before changing service entries.

Detailed baseline: `docs/GBP_BASELINE_2026-10-24.md`.

### GA4 / Search Console

The correct Dr. Farah production GA4 and Search Console sources are not yet connected/verified in the current project data workflow.

These are the next access gaps to resolve.

---

## 4. Current blockers / dependencies

### B-001 — Booking/Brevo delivery

**State:** RESOLVED / CLOSED  
**Evidence:** owner confirmation on 2026-10-24 that the website email/Brevo problem is fixed.  
**Reopen only if:** new production evidence shows booking notification failure/regression.

### B-002 — Measurement implementation not yet live

**State:** IN_PROGRESS  
**Class:** HARD for paid relaunch  
**Still needed:** runtime tracker validation, GA4 property/data stream, source/UTM/GCLID persistence, conversion implementation, `visit_completed` linkage/import, privacy/cookie alignment and end-to-end validation.

### B-003 — GA4 production access/property unresolved

**State:** READY  
**Class:** HARD for complete measurement baseline; SOFT for Ads/GBP forensic work  
**Unblock evidence:** correct Dr. Farah property/data stream identified/authorized/connected and test data visible.

### B-004 — Search Console production access/property unresolved

**State:** READY  
**Class:** HARD for BG30-04; SOFT for Ads/GBP work  
**Unblock evidence:** correct `drfarahvipurgentcare.com` property verified/authorized/connected and sitemap/indexing data readable.

### B-005 — Final Project Source replacement

**State:** WAITING_OWNER  
**Class:** not a blocker for project work; required only to complete cleanup of the ChatGPT Project configuration  
**Unblock evidence:** owner replaces current Project Source files with the final minimal single-workspace router pack.

---

## 5. Exact next actions after Project Source replacement

1. Resolve/verify the correct Dr. Farah GA4 property/data stream and connect it to the project workflow.
2. Resolve/verify the production Search Console property and connect it.
3. Complete runtime tag inventory and finalize Google tag/GA4 architecture.
4. Implement source/UTM/GCLID persistence and the compact conversion model.
5. Implement and validate `visit_completed` attribution/import.
6. Update privacy/cookie/tracking disclosures to match the implemented architecture.
7. Complete the Google Ads historical forensic audit.
8. Complete GBP/Search/local baseline and high-confidence corrections.
9. Proceed through the master roadmap in priority/gate order.

Safe parallel work remains available in Ads forensic analysis, GBP/reputation analysis, competitor/query research, source taxonomy, economics, Traveler/Pre-Op baseline work and content research.

---

## 6. Do not do yet

- do not launch or materially scale Google Ads while `G2-MEASUREMENT-READY` is red;
- do not optimize Ads toward low-quality Google-hosted actions as if they equal completed patients;
- do not bulk-delete GBP services merely because the catalogue is large;
- do not create a second roadmap;
- do not recreate deleted specialized ChatGPT tabs as project memory;
- do not invent unknown OpenProject identifiers;
- do not send unnecessary clinical-record detail to analytics/ad platforms;
- do not leave a material project result only in chat.

---

## 7. Resume protocol for every future context

Read, in order:

1. `README.md` on `dev`;
2. this `PROJECT_HANDOFF.md`;
3. `ROADMAP.md` current priority queue + relevant phase;
4. `docs/DECISIONS.md` when approval/strategy matters;
5. relevant dated baseline/spec/runbook/code only as needed;
6. live system when current state may have changed;
7. OpenProject when live work-package metadata matters.

Then:

1. re-check open blockers/dependencies;
2. select the highest-priority READY task without an unsatisfied HARD dependency;
3. execute and validate;
4. record durable evidence;
5. update this handoff before ending material work.

No deleted ChatGPT tab or old chat context is required to continue the project.