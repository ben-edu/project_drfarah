# Dr. Farah VIP Urgent Care — Unified Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Primary working branch:** `dev`  
> **Roadmap role:** durable sequencing, gates, dependencies, evidence and restart points  
> **OpenProject role:** live work-package status, assignment, dates, dependencies and completion  
> **Chat role:** analysis and execution interface only; chat history is never the durable source of truth

## 1. Purpose

This roadmap consolidates the website, booking, Google marketing, local SEO,
reputation, traveler/VIP, pre-op referral, content, service-economics,
analytics/growth-intelligence, governance and compliance work that was
previously distributed across multiple ChatGPT tabs.

The project should now be operated from one ChatGPT workspace, with GitHub as
the durable project memory and OpenProject as the live execution/status system.

The roadmap is intentionally **gate-based rather than strictly linear**. A blocked
step may be placed on hold while another safe, independent step advances. The
project must preserve the blocker, the dependency and the exact restart
condition instead of silently abandoning the blocked work.

## 2. Authority hierarchy

When sources disagree, use this order:

1. Current verified clinic/business fact from Dr. Farah or authoritative clinic record.
2. Live production system/account for its own current configuration and data.
3. Current approved decision in `docs/DECISIONS.md`.
4. Current repository roadmap/handoff/project documentation.
5. OpenProject for live work-package execution metadata.
6. Historical source packs, reports and prior chat conclusions.

Special cases:

- **Website/code/deployment:** GitHub + Jenkins + live environment evidence.
- **Google Ads:** live Google Ads account.
- **Google Business Profile:** live verified profile.
- **Organic Search:** live Google Search Console + live site.
- **Booking status:** clinic booking/admin system.
- **Work-package state:** OpenProject.

## 3. Operating states

Every roadmap item uses one of these states:

- `NOT_STARTED`
- `READY`
- `IN_PROGRESS`
- `BLOCKED`
- `PAUSED`
- `WAITING_EXTERNAL`
- `VALIDATING`
- `DONE`
- `DEFERRED`
- `CANCELLED`

`BLOCKED` means a dependency prevents progress.  
`PAUSED` means the work can continue but has intentionally yielded priority.  
`WAITING_EXTERNAL` means action is pending on a provider, clinic approval, external account or third party.

No item is marked `DONE` merely because code was written, a recommendation was made, or an account setting was changed. Its acceptance evidence must exist.

## 4. Blocked-step bypass mechanism

When an item cannot proceed:

1. Record the blocker in `HANDOFF.md`.
2. Record the dependency and evidence required to unblock it.
3. Mark whether the blocker is `hard` or `soft`.
   - `hard`: downstream work would create rework, bad data, compliance risk or unsafe production behavior.
   - `soft`: downstream independent work may safely continue.
4. Identify the next highest-priority `READY` item with no hard dependency.
5. Continue there without changing the blocked item's intended acceptance criteria.
6. At every handoff update, re-evaluate blocked items before starting new lower-priority work.

This prevents one external issue from freezing the project while preserving sequence discipline.

## 5. Cross-project workstreams

The consolidated workstreams are:

| Code | Workstream | Durable purpose |
|---|---|---|
| BG-00 | Governance, Decisions & Measurement | authority, source taxonomy, decisions, KPI definitions |
| BG-10 | Website & Conversion | public site, booking UX, landing pages, technical SEO, tracking implementation |
| BG-20 | Google Ads & Paid Acquisition | pre-launch readiness, paid acquisition, search-term optimization, CAC |
| BG-30 | Google Business, Local SEO & Reputation | GBP, reviews, Search Console, Maps/local visibility |
| BG-40 | Hotel / Traveler / VIP Growth | traveler baseline, service model, partner pipeline, pilot |
| BG-50 | Pre-Op Referral Engine | baseline, economics, referral proposition, target practices, pilot |
| BG-60 | Video, Social & Creative | reusable physician-led content system |
| BG-70 | Service Priority & Economics | service-level value, margin, capacity and acquisition priority |
| BG-80 | Analytics & Growth Intelligence | source-to-booking-to-completed-visit attribution and reporting |
| BG-90 | Operations / Compliance Readiness | claims, privacy, capacity, mobile/traveler readiness and compliance triggers |

OpenProject keeps the exact work-package hierarchy and live status. This file
keeps the cross-workstream execution order.

---

# Phase 0 — Stabilize Core Conversion Infrastructure

**Goal:** do not send paid traffic into a broken or unmeasurable conversion path.

## P0.1 — Resolve booking/email delivery incident

**Primary owner/workstream:** BG-10 / website operations  
**Current known issue:** Brevo-related booking email delivery is under active remediation in a separate technical workflow.

Acceptance evidence:

- production booking submission succeeds;
- appointment persistence is verified;
- expected clinic email delivery is verified with a controlled receipt test;
- failure behavior is observable and does not silently lose the booking;
- current production configuration is documented without exposing secrets.

**Gate:** `G0-BOOKING-HEALTHY`

Paid advertising must not launch before this gate is green.

## P0.2 — Inventory current site measurement stack

Determine, with production evidence:

- whether Google tag is present;
- whether GA4 is present and which property is used;
- whether Google Tag Manager is present;
- whether duplicate tags exist;
- current cookie/consent behavior where applicable;
- current UTM/source/partner propagation;
- which booking events are already instrumented;
- whether click-to-call and other high-value actions are measurable.

Deliverable: a dated tag/measurement inventory.

## P0.3 — Define canonical conversion ladder

Required business ladder:

`Visit → Qualified Contact → Booking → Confirmed Appointment → Completed Visit → Collected Revenue → Contribution / Repeat / Referral Value`

Classify web/ad events as diagnostic or business outcome events.

**Gate:** `G0-MEASUREMENT-SPEC-APPROVED`

---

# Phase 1 — Implement and Validate Measurement Foundation

**Goal:** create reliable first-party measurement before first paid-media launch.

## P1.1 — Google tag / GA4 architecture

Choose the smallest non-duplicative implementation based on P0.2.

Requirements:

- production and staging remain distinct;
- staging does not pollute production analytics;
- no unnecessary patient/clinical data is transmitted;
- source/campaign/partner context is preserved;
- deployment follows repository/Jenkins rules.

## P1.2 — Booking conversion instrumentation

Instrument and validate, as applicable:

- booking start;
- service selection;
- availability view;
- slot selection;
- booking created;
- click-to-call;
- other approved primary CTA events.

Do not define every event as a primary Google Ads conversion.

## P1.3 — Google Ads conversion architecture

Audit all existing conversion actions and decide:

- primary vs secondary;
- exact source;
- counting method;
- value treatment;
- attribution setting;
- conversion window;
- diagnostic vs business-outcome role.

Known account baseline to verify live:

- Customer ID `652-510-3588`;
- USD;
- Pacific Time;
- created May 2025;
- no confirmed campaign spend/history to date;
- existing phone/contact conversion actions require configuration verification.

## P1.4 — End-to-end validation

Test a controlled journey from acquisition parameters through booking creation
and analytics/event visibility.

Acceptance evidence:

- source parameters survive the intended journey;
- a test booking is visible in the booking system;
- expected analytics events are visible;
- Google Ads conversion path is technically ready;
- no duplicate conversion firing;
- no patient clinical data appears in marketing payloads.

**Gate:** `G1-MEASUREMENT-READY`

No non-trivial paid campaign launch before this gate.

---

# Phase 2 — Establish Google Account Baselines

This phase can begin while Phase 0/1 technical work is progressing, because most
of it is read-only.

## P2.1 — Connect/read authorized marketing accounts

Preferred read integration: Windsor.ai where useful.

Connect or otherwise verify access to:

- Google Ads;
- Google Business Profile;
- GA4;
- Google Search Console.

Writes require explicit confirmation for the exact change.

## P2.2 — BG20 pre-launch Google Ads audit

Because no confirmed campaigns have run, treat current work as **pre-launch
configuration and measurement readiness**, not historical performance analysis.

Audit:

- account identity and history;
- linked systems;
- conversion goals;
- draft/paused campaigns;
- keywords and match types;
- negative keywords/shared lists;
- geographic targeting/exclusions;
- Presence vs Presence-or-Interest settings;
- language targeting;
- ad schedule;
- assets and landing pages;
- automated rules and their enabled state;
- change history;
- healthcare-policy-sensitive services.

**Output:** `KEEP / FIX / REMOVE / CREATE / TEST / MEASURE_FIRST / POLICY_REVIEW / NO_ACTION` recommendations.

## P2.3 — BG30 Google Business Profile baseline

Before broad edits, capture:

- public name;
- verification/ownership;
- clinic vs practitioner profile structure;
- possible duplicates;
- address/map pin;
- phone;
- website/booking links;
- categories;
- services;
- hours and special hours;
- service area;
- description;
- photos/video;
- rating/review count;
- reviews/replies;
- warnings/notices;
- available performance metrics.

Current owner-provided evidence to re-verify live:

- rating: `5.0`;
- review count: `108`;
- regular clinic hours: Monday–Friday, 8:30 AM–5:30 PM Pacific;
- last patient accepted before 5:00 PM.

## P2.4 — Search Console / organic baseline

Audit:

- correct production property;
- verification;
- sitemap;
- indexing;
- clicks/impressions/CTR;
- top queries/pages;
- brand vs non-brand patterns;
- urgent, pre-op, traveler/mobile and relevant service themes;
- technical SEO handoffs.

**Gate:** `G2-GOOGLE-BASELINES-CAPTURED`

---

# Phase 3 — Correct High-Confidence Baseline Problems

**Goal:** fix verified problems before experimentation.

Priority order:

1. factual/policy/eligibility risk;
2. broken conversion or tracking;
3. broken links/booking paths;
4. wrong hours/location/contact details;
5. duplicate-profile risk;
6. category/service misrepresentation;
7. poor landing-page/search-intent alignment;
8. measurement gaps.

Every material change requires:

- before state;
- evidence;
- proposed change;
- approval requirement;
- implementation date;
- post-change validation.

**Gate:** `G3-FOUNDATION-CORRECTED`

---

# Phase 4 — Market and Demand Intelligence

This phase may run in parallel with Phase 3 when no hard dependency exists.

## P4.1 — Paid search demand and keyword research

For each candidate service/intention determine:

- plausible query themes;
- local demand;
- estimated competition/cost where available;
- policy sensitivity;
- page readiness;
- conversion readiness;
- economics/capacity dependencies.

## P4.2 — Beverly Hills local Search / Maps competitor baseline

Use a controlled query set and documented location/method.

Initial themes:

- urgent care / same-day doctor;
- pre-op clearance;
- traveler/hotel/mobile where operationally valid.

Do not present one manual search as universal ranking.

## P4.3 — Reputation analysis

Analyze review themes and workflow.

Current selected testimonial candidates include Marie C., Lissette A., Olga
Kirpicheva (Liv), Frank Salmoon, Pooja Nair and wipa. Website reuse must preserve
meaning and follow the approved privacy/authenticity standard.

## P4.4 — Service prioritization dependency

Use BG-70 logic before substantial acquisition investment:

- demand;
- collected revenue;
- variable cost;
- physician/staff time;
- capacity;
- repeat/referral leverage;
- acquisition cost;
- compliance.

**Gate:** `G4-ACQUISITION-PRIORITIES-DECIDED`

---

# Phase 5 — Landing Pages and Conversion Readiness

**Goal:** match acquisition intent to a usable conversion destination.

Candidate page requirements may include:

- urgent/same-day;
- pre-op;
- traveler/VIP;
- selected priority services.

Each handoff to BG-10 must include:

- evidence;
- affected URL/page;
- exact requirement;
- message/intent;
- CTA;
- tracking requirement;
- primary KPI;
- claims requiring Dr. Farah approval.

Do not create service pages merely to increase page count.

**Gate:** `G5-LANDING-PATHS-READY`

---

# Phase 6 — First Controlled Google Ads Launch

**Preconditions:** G0, G1 and applicable G3/G5 gates are green.

Candidate campaign order is a hypothesis, not a fixed decision:

1. Brand protection/measurement if evidence supports it;
2. urgent/same-day high-intent search;
3. pre-op consumer search after page/workflow readiness;
4. traveler/hotel search after BG-40/BG-90 operational readiness;
5. sensitive services only after current policy review.

Before launch define:

- hypothesis;
- audience/geography;
- campaign structure;
- keyword/match strategy;
- negatives;
- bidding approach;
- budget as a learning budget;
- primary conversion;
- landing page;
- stop/modify/scale rules;
- review date/evidence threshold.

**Gate:** `G6-FIRST-PAID-EXPERIMENT-LIVE`

---

# Phase 7 — Google Business / Reputation Growth System

Can proceed independently of paid-media launch once baseline and accuracy are
secured.

## P7.1 — Review acquisition workflow

Rules:

- neutral genuine-experience request;
- no gating;
- no incentives;
- no five-star request;
- no fake engagement;
- privacy-safe responses.

Track review requests, new reviews, velocity, rating, response rate/time and themes.

## P7.2 — GBP improvement cycle

Prioritize accurate categories, services, links, hours, imagery, action paths and
approved content. Avoid keyword-stuffed names or duplicate profiles.

## P7.3 — Local SEO improvement cycle

Use Search Console + GBP + competitor evidence to create concrete BG-10
requirements rather than generic SEO tasks.

**Gate:** `G7-LOCAL-GROWTH-CYCLE-LIVE`

---

# Phase 8 — Traveler / Hotel / VIP Growth

Consolidates BG-40.

Sequence:

1. establish traveler baseline;
2. separate traveler status from acquisition source;
3. identify existing hotel/concierge sources;
4. define clinic/mobile/telemedicine service and response model;
5. interview selected partners;
6. build prioritized target list;
7. define partner kit and attribution;
8. run a small measurable pilot;
9. evaluate completed visits, revenue, repeat referral and operational burden.

Hard dependencies include BG-90 operational readiness for mobile/hotel promises
and BG-80 attribution for partner/source measurement.

---

# Phase 9 — Pre-Op Referral Engine

Consolidates BG-50.

Sequence:

1. establish current pre-op baseline;
2. validate referral economics;
3. define referrer/patient value proposition;
4. identify existing/warm referrers;
5. build prioritized surgeon/surgery-center database;
6. define referral package and workflow;
7. approve turnaround/claims/privacy boundaries;
8. launch small outreach pilot;
9. measure active referring practices, completed clearances, repeat referrals,
   revenue, turnaround and acquisition cost.

No referral-compensation structure without BG-90 legal/compliance trigger.

---

# Phase 10 — Physician-Led Content System

Consolidates BG-60.

Sequence:

1. choose audience/business questions;
2. define first batch pillars;
3. prepare shoot/asset plan;
4. prepare clinically reviewed talking points;
5. film master assets;
6. organize source library;
7. create long/short/website/paid derivatives;
8. publish approved assets;
9. measure qualified traffic, booking assistance and business usefulness;
10. establish repeatable batch cycle only after first-batch learning.

Content should be fed by evidence from Ads search terms, Search Console, reviews,
traveler interviews, pre-op questions and website friction.

---

# Phase 11 — Growth Intelligence / Attribution

Consolidates BG-80 and the existing Growth Intelligence handoff.

Initial objective:

`Source / Campaign / Partner → Booking → Confirmed → Completed → Revenue`

Use data minimization and opaque linkage. Do not create a second clinical record.

Recommended technical sequence:

1. approved source taxonomy;
2. first-party marketing session;
3. constrained event vocabulary;
4. booking attribution linkage;
5. booking outcome synchronization;
6. Google Ads read-only cost ingestion;
7. partner/referral linkage;
8. analytical views;
9. dashboard and weekly review;
10. AI analyst/recommendation layer;
11. controlled write automation only after explicit later approval.

---

# Phase 12 — Recurring Growth Operating Cycle

Once the foundations and at least one live acquisition experiment exist, run:

## Weekly

- website/booking health;
- Google Ads spend/search terms/conversion quality;
- GBP/review changes;
- acquisition-source coverage;
- experiment blockers;
- urgent operational issues.

## Monthly

- completed visits by source;
- CAC by source/campaign where defensible;
- collected revenue;
- local/organic performance;
- partner/referral output;
- service economics;
- capacity constraints;
- experiment decisions.

Decision vocabulary:

`SCALE / MODIFY / STOP / CONTINUE_MEASURING / MEASURE_FIRST / NO_ACTION`

---

# 6. Current priority queue — 2026-10-21

This is the initial ordering and must be refreshed in `HANDOFF.md` after every
material session.

| Priority | Item | State | Hard dependency / note |
|---:|---|---|---|
| 0 | Booking/Brevo production delivery verification | IN_PROGRESS | separate technical workflow; hard gate for paid launch |
| 1 | Production tag/analytics inventory | READY | can run while booking issue is being fixed |
| 2 | Define/approve conversion measurement specification | READY | depends on current booking flow understanding |
| 3 | Connect/verify Google Ads, GBP, GA4, Search Console access | READY | read-only baseline work |
| 4 | Google Ads pre-launch configuration audit | READY | no campaign launch required |
| 5 | GBP baseline and duplicate/category/service audit | READY | read-only first |
| 6 | Search Console organic/indexing baseline | READY after access | independent of Ads launch |
| 7 | Implement/validate measurement stack | WAITING on P0.2/P0.3 | hard launch dependency |
| 8 | Correct verified Google/website foundation issues | NOT_STARTED | requires audit findings |
| 9 | Keyword/local competitor/service-priority research | NOT_STARTED | can overlap corrections |
| 10 | Landing-page requirements and implementation | NOT_STARTED | evidence-driven |
| 11 | First controlled Google Ads experiment | BLOCKED | requires booking + measurement gates |
| 12 | Review acquisition/reputation operating cycle | NOT_STARTED | GBP baseline first |
| 13 | Traveler/VIP growth pilot | NOT_STARTED | baseline + operations + attribution |
| 14 | Pre-op referral pilot | NOT_STARTED | baseline + proposition + package |
| 15 | Physician-led content batch | NOT_STARTED | business priorities + approvals |
| 16 | Growth Intelligence MVP | NOT_STARTED | measurement requirements must stabilize |

## 7. Definition of a roadmap update

At the end of every material work session:

1. Update `HANDOFF.md` first.
2. If sequence/gates changed, update this `ROADMAP.md`.
3. If an approved decision changed, update `docs/DECISIONS.md`.
4. If stable project facts changed, update `PROJECT.md`.
5. Append one short dated record to `SESSION_LOG.md`.
6. Link the relevant OpenProject work package/evidence when known.
7. Never leave a material decision only in chat.

## 8. Definition of resume-ready

A new ChatGPT session or human operator must be able to read, in order:

1. `README.md`
2. `HANDOFF.md`
3. `ROADMAP.md`
4. `docs/DECISIONS.md`
5. `PROJECT.md` only when deeper stable context is required

and answer:

- what is true now;
- what is blocked;
- what is being worked on;
- what should happen next;
- what evidence is required;
- which OpenProject work package owns the execution state.

If those questions cannot be answered, the documentation is stale and must be
updated before substantial new work starts.
