# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **This is the live cross-workstream resume document.**  
> Update this file after every material project session.  
> Historical website/deployment notes remain in `HANDOFF.md`; use this file for current unified project control.

**Last updated:** 2026-10-21  
**Repository:** `ben-edu/project_drfarah`  
**Default/integration branch:** `dev`  
**Roadmap:** `ROADMAP.md`  
**Operating model:** `docs/PROJECT_OPERATING_MODEL.md`  
**Business/growth source:** `docs/BUSINESS_GROWTH_SOURCE.md`  
**Measurement baseline:** `docs/MEASUREMENT_BASELINE_2026-10-21.md`  
**Conversion specification:** `docs/CONVERSION_MEASUREMENT_SPEC.md`

---

## 1. Current project-control decision

`DECISION:` Consolidate the former multiple ChatGPT workstream tabs into one
active project chat.

GitHub becomes the durable project memory for roadmap, handoff, decisions,
project facts, code and implementation evidence.

OpenProject remains authoritative for live work-package status, assignment,
dates, dependencies, milestones and completion.

The active chat is an analysis/execution interface, not the durable source of
truth.

## 2. Current strategic focus

The immediate project focus is **conversion infrastructure and Google marketing
readiness**, while preserving ongoing website/booking remediation.

Do not begin by spending on Google Ads.

Current intended sequence:

`Booking health → Measurement inventory → Conversion specification → Google account baselines → Measurement implementation/validation → Foundation corrections → Demand/landing-page work → First controlled paid experiment`

Independent read-only work on Google Ads, GBP and Search Console may proceed in
parallel while booking/email remediation is unresolved.

## 3. Current verified / owner-provided facts

### Business

- Dr. Farah VIP Urgent Care
- 9229 Wilshire Blvd., Beverly Hills, CA 90210
- Phone: 310-467-0101
- Fax: 707-261-0739
- Regular hours: Monday–Friday 8:30 AM–5:30 PM Pacific Time
- Last patient accepted before 5:00 PM

### Repository / deployment

- repository: `ben-edu/project_drfarah`
- `dev` is integration/staging branch
- `main` is production branch
- Jenkins remains deployment authority
- current website/booking technical history remains documented in `HANDOFF.md`

### Booking/email

`BLOCKER:` Brevo-related booking email delivery is under active technical
remediation in a separate workflow.

This is a **hard dependency for first paid-media launch** but a **soft dependency
for read-only account audits, local SEO analysis, keyword research and baseline
capture**.

Do not claim resolved until controlled production booking and expected receipt
evidence exist.

### Website measurement — source audit completed, runtime validation pending

`FACT:` repository/source inspection on 2026-10-21 found no implemented Google
measurement stack in `dev` or the inspected production-branch frontend source.

No repository evidence was found for:

- Google tag / `gtag.js`;
- Google Tag Manager;
- GA4 page/event instrumentation;
- Google Ads website conversion tags;
- `dataLayer` event pushes;
- click-to-call analytics;
- booking-funnel analytics events.

`FACT:` `scripts/prepare-production-frontend.sh` does not inject analytics or
advertising tags during production assembly.

`FACT:` the booking flow currently preserves only a coarse first-party source
marker using `source`, `partner` or `utm_source`, collapsed into
`appointments.source` (`String(32)`).

`FACT:` the current privacy page states that the site uses only essential
cookies and does not set advertising or third-party tracking cookies. It is
also explicitly marked as draft pending clinic/legal review.

`RISK:` adding analytics/Ads tags without updating the privacy/consent design
would create a mismatch between actual site behavior and published privacy copy.

`RISK:` staging and production use the same frontend source. Analytics must be
environment-isolated before deployment so staging does not pollute production
data.

Detailed evidence and recommended architecture are recorded in
`docs/MEASUREMENT_BASELINE_2026-10-21.md`.

Remaining evidence to close P0.2:

- browser/network-level validation of the deployed production site;
- verification of any provider-side tag configuration not represented in Git;
- verification of whether a production GA4 property already exists;
- approved privacy/consent approach for the chosen measurement architecture.

### Canonical conversion measurement — draft completed

`FACT:` `docs/CONVERSION_MEASUREMENT_SPEC.md` now defines the first canonical
measurement contract.

Important definitions:

- `booking_request_created` fires only after the booking API returns HTTP 201;
- it represents a pending appointment request, **not** a confirmed appointment;
- `click_to_call` is a lead signal, not a qualified call;
- diagnostic funnel events must not all become primary Google Ads conversions;
- long-term optimization should move toward `visit_completed` or another
  higher-quality business outcome when reliable reconciliation is available;
- patient form values and clinical details are excluded from marketing payloads;
- staging must not contaminate production analytics.

The specification is `DRAFT_FOR_VALIDATION` until live Google Ads conversion
settings, GA4 property, call-tracking capability and privacy/consent design are
verified.

### Google Ads

Owner-provided baseline to verify live:

- Customer ID: `652-510-3588`
- account name: Dr Farah VIP Urgent Care
- currency: USD
- timezone: Pacific Time
- no MCC reported
- created May 2025
- no confirmed campaigns have run yet

Therefore current Ads work is **pre-launch configuration and measurement
readiness**, not historical performance optimization.

Known reported conversion actions require exact live verification.

### Google Business Profile

Latest owner-provided screenshots showed:

- rating: 5.0
- reviews: 108

Re-verify live before using as a current KPI.

Current review themes include attentive/thorough physician care,
professionalism, compassion, efficient visits, communication, follow-up and
friendly staff.

### Connected data tools

A Windsor.ai inspection on 2026-10-21 found only unrelated Search Console
properties currently connected in this ChatGPT/Windsor context. Dr. Farah's
Google Ads, GBP, GA4 and production Search Console sources were not yet connected
through Windsor.ai at that check.

This does not mean the underlying Google accounts are inaccessible; Behnam now
has direct admin access to Google Ads and Google Business Profile.

## 4. Current priority queue

| Priority | Work | State | Dependency / acceptance |
|---:|---|---|---|
| 0 | Resolve and verify booking/Brevo production delivery | IN_PROGRESS | controlled production booking + expected receipt evidence |
| 1 | Audit production measurement/tag stack | VALIDATING | source audit complete; runtime/browser validation + provider/account checks remain |
| 2 | Define canonical conversion measurement specification | VALIDATING | draft complete; validate against live Ads/GA4/call/privacy setup |
| 3 | Verify/connect Google Ads, GBP, GA4, Search Console data access | READY | read-first; no broad writes |
| 4 | Run Google Ads pre-launch configuration audit | READY | live account evidence |
| 5 | Capture full GBP baseline | READY | preserve before-state before edits |
| 6 | Capture Search Console/indexing/local SEO baseline | READY after access | production property required |
| 7 | Implement and validate measurement stack | WAITING | account IDs + privacy/consent architecture + P0 validation required |
| 8 | Fix verified Google/website foundation issues | NOT_STARTED | audit evidence required |
| 9 | Run demand/keyword/local competitor/service-priority research | NOT_STARTED | can overlap P8 |
| 10 | Implement evidence-backed landing-page improvements | NOT_STARTED | formal BG-10 handoff |
| 11 | Launch first controlled Google Ads experiment | BLOCKED | booking + measurement + landing-page readiness |
| 12 | Establish ongoing review/reputation cycle | NOT_STARTED | GBP baseline first |
| 13+ | Traveler, Pre-Op, Content and Growth Intelligence pilots | NOT_STARTED | see ROADMAP.md gates |

## 5. Exact next actions

### Next Action A — close P0.2 runtime validation

Workstream: BG-10 / BG-20 / BG-80

Repository/source inventory is complete and documented.

Remaining checks:

1. validate deployed production HTML/network behavior in a current browser;
2. verify that no Google/third-party measurement is being injected outside Git;
3. verify any existing production GA4 property and measurement ID;
4. document current consent/cookie behavior against actual planned measurement.

Deliverable: P0.2 accepted baseline or explicit remaining external blocker.

### Next Action B — validate P0.3 conversion specification

Workstream: BG-00 / BG-10 / BG-20 / BG-80

Use `docs/CONVERSION_MEASUREMENT_SPEC.md` as the draft contract.

Validate it against:

1. live Google Ads conversion actions/goals;
2. actual GA4 property/data stream if one exists;
3. call-tracking capability;
4. approved privacy/cookie/consent approach;
5. booking outcome fields available for confirmed/completed reconciliation.

Do not implement tags until this validation identifies the exact production IDs
and approved consent behavior.

### Next Action C — Google Ads account baseline

Workstream: BG-20

Read and record without broad changes:

1. account identity/history;
2. linked products;
3. all conversion actions/goals;
4. drafts/paused/removed campaigns;
5. keywords/match types/negatives;
6. geography and location options;
7. language/ad schedule;
8. automated rules and enabled state;
9. change history;
10. landing URLs/assets;
11. policy-sensitive service exposure.

### Next Action D — GBP baseline

Workstream: BG-30

Capture:

1. exact public profile name;
2. verification/ownership;
3. practitioner/clinic/duplicate structure;
4. categories;
5. services;
6. hours/special hours;
7. links;
8. service area;
9. description;
10. imagery;
11. reviews/replies;
12. available performance data;
13. warnings/notices.

### Next Action E — Search Console baseline

Workstream: BG-30 / BG-10

Once correct production property access is confirmed:

- indexing/sitemap;
- top queries/pages;
- branded vs non-branded;
- urgent/pre-op/traveler themes;
- technical SEO issues requiring website changes.

## 6. Safe parallel work while booking issue is open

The following work may continue safely:

- read-only Google Ads configuration audit;
- read-only GBP baseline;
- Search Console baseline;
- keyword/demand research;
- competitor/local visibility research;
- review/reputation analysis;
- conversion measurement design;
- service-priority/economics data requests;
- traveler/pre-op baseline data collection.

Do not launch meaningful paid traffic until booking and measurement gates are
satisfied.

## 7. Do not do yet

- Do not launch or materially scale Google Ads.
- Do not install production tracking without an approved measurement/privacy approach.
- Do not treat existing Google conversion actions as valid business conversions until audited.
- Do not broadly restructure Google Ads before the account baseline is captured.
- Do not make broad GBP edits before the baseline/duplicate check is captured.
- Do not enable sensitive healthcare advertising without current policy review.
- Do not upload patient health data to marketing platforms.
- Do not create many new landing pages without demand/business evidence.
- Do not build the Growth Intelligence Platform before the source/conversion contract is sufficiently stable.

## 8. Blocker register

### B-001 — Booking/Brevo delivery

**State:** IN_PROGRESS  
**Type:** hard for paid launch / soft for account research  
**Evidence needed to close:** controlled production booking persists and expected
clinic/patient delivery behavior is verified.  
**Current technical source:** `docs/EMAIL_DELIVERY_RUNBOOK.md` + active PR/workflow evidence.

### B-002 — Marketing measurement implementation/readiness

**State:** IN_PROGRESS / NARROWED  
**Type:** hard for paid launch  
**Evidence established:** repository source contains no Google tag, GTM, GA4 or
booking/call analytics implementation; production assembly does not inject them.  
**Evidence still needed to close:** browser/network runtime validation,
production GA4/account identifiers, approved consent/privacy approach, then
end-to-end event validation after implementation.  
**Current sources:** `docs/MEASUREMENT_BASELINE_2026-10-21.md`,
`docs/CONVERSION_MEASUREMENT_SPEC.md`.

### B-003 — Google account baseline incomplete

**State:** READY TO INVESTIGATE  
**Type:** hard for account launch decisions, soft for website work  
**Evidence needed to close:** current Ads/GBP/GA4/Search Console configuration
snapshot.

## 9. Decision / handoff rules

After any material action:

1. update this file;
2. update `ROADMAP.md` if sequence/gate/state changed materially;
3. update `docs/DECISIONS.md` if a decision was explicitly approved;
4. update `PROJECT.md` only if a durable project fact/scope/architecture changed;
5. update OpenProject work-package state/evidence separately when applicable;
6. never leave a material result only in chat.

For website work generated by marketing analysis, use the Marketing → Website
handoff format in `docs/PROJECT_OPERATING_MODEL.md`.

## 10. OpenProject continuity

The old workstream identities remain valid even though their separate chat tabs
will be retired:

- BG-00 Governance, Decisions & Measurement
- BG-10 Website & Conversion
- BG-20 Google Ads & Paid Acquisition
- BG-30 Google Business, Local SEO & Reputation
- BG-40 Hotel / Traveler / VIP Growth
- BG-50 Pre-Op Referral Engine
- BG-60 Video, Social & Creative
- BG-70 Service Priority & Economics
- BG-80 Analytics & Growth Intelligence
- BG-90 Operations / Compliance Readiness

Do not infer a live OpenProject work-package status from this handoff. Query or
use OpenProject evidence when status matters.

## 11. Resume instruction for the next session

Read:

1. this file;
2. `ROADMAP.md` current-priority section;
3. `docs/DECISIONS.md` if a decision/approval is involved;
4. relevant runbook/source file only as needed.

Then start with the highest `READY` item that is not blocked by a hard
dependency. Re-check B-001/B-002/B-003 before creating lower-priority new work.
