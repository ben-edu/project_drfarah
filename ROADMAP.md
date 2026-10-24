# Dr. Farah VIP Urgent Care — Master Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Canonical roadmap:** this file only  
> **Integration/default branch:** `dev`  
> **Active ChatGPT workspace:** the existing `BG-20` project tab, now serving as the single unified project workspace  
> **OpenProject:** authoritative for live work-package status, assignee, dates, dependencies, milestones and completion  
> **GitHub:** durable project memory, roadmap, handoff, decisions, code, runbooks and evidence  
> **Live systems:** authoritative for their own current configuration and performance

---

## 1. Purpose and consolidation decision

This is the **single master roadmap** for the Dr. Farah project.

It consolidates:

- website and booking development/stabilization;
- governance and measurement;
- Google Ads and paid acquisition;
- Google Business Profile, Local SEO and reputation;
- traveler / hotel / VIP growth;
- pre-operative referral growth;
- physician-led video/social/creative;
- service-priority and economics work;
- analytics, attribution and Growth Intelligence;
- operational, privacy and compliance readiness;
- the work that was previously distributed across separate ChatGPT tabs aligned to OpenProject workstreams.

The unified control plane is now merged to `dev`. The separate project chat tabs may be retired after the minimal Project Sources are replaced to point to `dev` and a resume test confirms that this control plane is sufficient. Their work is **not cancelled**; it is represented below by workstream code, roadmap phase, dependencies and acceptance evidence.

No second roadmap should be created for website development, marketing, Growth Intelligence or another workstream. Detailed technical plans/runbooks may remain in their specialized files, but sequencing belongs here.

`PROJECT.md` remains the stable product/technical charter. `HANDOFF.md` remains historical/detailed website/deployment evidence. Neither is a competing roadmap.

---

## 2. Authority hierarchy

When sources disagree, use this order:

1. current verified clinic/business fact from Dr. Farah or authoritative clinic record;
2. live production/account system for its own current state;
3. approved decision in `docs/DECISIONS.md`;
4. current `PROJECT_HANDOFF.md` and this roadmap;
5. stable repository specifications/runbooks/code;
6. OpenProject for live execution metadata;
7. historical reports, old Project Sources and prior chat conclusions.

Special cases:

- website/code/deployment → GitHub + Jenkins + live environment evidence;
- Google Ads → live Google Ads account;
- Google Business Profile → live verified profile;
- organic Google Search → Search Console + live site;
- GA4 → live GA4 property/data stream;
- booking outcome → booking/admin platform;
- work-package state → OpenProject.

A newer verified fact supersedes an older Project Source statement. Example: live Google Ads evidence has superseded the former assumption that the account had no campaign history.

---

## 3. Project-control mechanism

### 3.1 Required operating states

Every roadmap item uses one state:

- `NOT_STARTED`
- `READY`
- `IN_PROGRESS`
- `VALIDATING`
- `BLOCKED`
- `PAUSED`
- `WAITING_EXTERNAL`
- `DONE`
- `DEFERRED`
- `CANCELLED`

`DONE` requires acceptance evidence, not merely a recommendation, code commit or account edit.

### 3.2 Blocker classes

Every blocker is classified as:

- **HARD** — downstream work would create invalid data, production risk, policy/compliance risk or significant rework;
- **SOFT** — the blocked item waits, but independent work may proceed safely.

For every blocked/paused item record in `PROJECT_HANDOFF.md`:

1. item/workstream;
2. reason;
3. hard vs soft;
4. evidence/action required to unblock;
5. downstream work prohibited while blocked;
6. safe parallel work;
7. exact restart point.

### 3.3 Next-task selection algorithm

At the start of every substantive session:

1. read `PROJECT_HANDOFF.md`;
2. re-check all HARD blockers;
3. choose the highest-priority `READY` item with no unsatisfied HARD dependency;
4. if an item becomes blocked, record it immediately and move to the next eligible item;
5. do not create lower-value work merely because a high-priority item is waiting;
6. after material work, update the handoff before ending the session.

This rule is what allows a future chat/context window/operator to resume precisely without relying on chat memory.

### 3.4 Material-session close protocol

A material session is incomplete until:

- verified facts/results are recorded in an appropriate GitHub file;
- `PROJECT_HANDOFF.md` is updated with state, evidence, blockers and exact next actions;
- this roadmap is updated only if sequencing/gates/scope changed;
- `docs/DECISIONS.md` is updated only for approved decisions;
- `SESSION_LOG.md` receives a concise historical entry where appropriate;
- OpenProject is updated separately when live work-package state/evidence changes.

No material result should live only in chat.

---

## 4. Workstream registry retained from the former tabs

| Code | Workstream | Durable purpose |
|---|---|---|
| BG-00 | Governance, Decisions & Measurement | authority, access, taxonomy, KPI and decision discipline |
| BG-10 | Website & Conversion | public site, booking, landing pages, technical SEO, tracking implementation |
| BG-20 | Google Ads & Paid Acquisition | historical forensic audit, corrections, relaunch and optimization |
| BG-30 | Google Business, Local SEO & Reputation | GBP, Search Console, reviews, Maps/local visibility |
| BG-40 | Hotel / Traveler / VIP Growth | traveler baseline, service model, partner pipeline and pilot |
| BG-50 | Pre-Op Referral Engine | baseline, economics, proposition, target practices and pilot |
| BG-60 | Video, Social & Creative | reusable physician-led content system |
| BG-70 | Service Priority & Economics | service value, margin, capacity and acquisition priority |
| BG-80 | Analytics & Growth Intelligence | full funnel, attribution, dashboards, reporting and experiments |
| BG-90 | Operations / Compliance Readiness | claims, privacy, capacity, mobile/hotel readiness and compliance triggers |

The workstream identities remain useful for OpenProject mapping and handoffs even though only one ChatGPT tab remains active.

---

## 5. Master gates

| Gate | Meaning | Minimum evidence |
|---|---|---|
| `G0-CONTROL-PLANE-LIVE` | GitHub can carry project continuity without old tabs | roadmap + handoff + decisions on `dev` + minimal Project Sources pointing to `dev` + successful resume test |
| `G1-BOOKING-HEALTHY` | booking path is operationally safe | production booking persists + expected notification behavior verified |
| `G2-MEASUREMENT-READY` | acquisition can be measured without duplicate/bad data | GA4/tag architecture + attribution + key conversions tested |
| `G3-GOOGLE-BASELINES-CAPTURED` | Ads/GBP/SC/GA4 current state known | dated baselines from live systems |
| `G4-FOUNDATION-CORRECTED` | high-confidence factual/technical/policy issues corrected | before/after evidence |
| `G5-ECONOMICS-AND-PRIORITIES-READY` | acquisition priorities can be judged economically | source/service baseline + priority matrix |
| `G6-LANDING-PATHS-READY` | intended acquisition traffic has fit-for-purpose destinations | approved page/CTA/tracking paths |
| `G7-FIRST-PAID-EXPERIMENT-LIVE` | controlled paid relaunch started | launch spec + budget + measurement + stop/scale rules |
| `G8-LOCAL-GROWTH-CYCLE-LIVE` | GBP/reputation/local SEO operating cycle established | workflow + baseline + measurement cadence |
| `G9-FIRST-PARTNERSHIP-EXPERIMENTS-LIVE` | traveler/pre-op pilots running where validated | operational/compliance + attribution + pilot spec |
| `G10-CONTENT-ENGINE-LIVE` | first reusable content batch published/measured | approved asset system + distribution + performance review |
| `G11-GROWTH-INTELLIGENCE-BASELINE-LIVE` | source→visit outcome reporting operational | attribution joins + dashboard/reporting + quality checks |
| `G12-REPEATABLE-GROWTH-CYCLE` | scale/modify/stop cadence is routine | recurring reviews tied to business outcomes |

---

# Phase 0 — Consolidate the Project Control Plane

**Objective:** make project continuity independent of any single ChatGPT context window.

### P0.1 — Merge the unified control plane to `dev`

**State:** `DONE`  
**Primary workstreams:** BG-00 / project control  
**Acceptance evidence:** PR #78 merged to `dev` on 2026-10-24; squash merge `c10b7bec5f9acad0531b88bac9056d4950d918a6`.

Required:

- one `ROADMAP.md` in the repository;
- one current `PROJECT_HANDOFF.md`;
- `docs/DECISIONS.md` for approved decisions;
- `docs/PROJECT_OPERATING_MODEL.md` for operating rules;
- `docs/BUSINESS_GROWTH_SOURCE.md` for compact durable business context;
- README reading order;
- no contradictory roadmap file.

### P0.2 — Replace Project Sources with minimal GitHub routers

**State:** `IN_PROGRESS`

The uploaded ChatGPT Project `.md` sources should contain only:

- GitHub repository identity;
- authority hierarchy;
- session start/resume instructions;
- workstream routing;
- privacy/data-use principle;
- explicit statement that GitHub/live systems supersede Project Sources.

They must not become a parallel business database.

### P0.3 — Retire specialized ChatGPT tabs

**State:** `WAITING_EXTERNAL` until P0.2 and the resume test are complete.

After P0.1/P0.2 are verified:

- keep the existing BG-20 tab as the single active project workspace;
- retire/delete the other specialized project tabs at the owner's discretion;
- continue referencing BG-00 through BG-90 as logical/OpenProject workstreams.

### P0.4 — BG00-01 Validate OpenProject Project Access & Membership

Preserve the prior BG-00 requirement:

- correct OpenProject project identified;
- Behnam/Dr. Farah membership and permissions verified where current evidence is available;
- workstream/milestone structure mapped;
- no role change made merely because a difference is observed.

### P0.5 — BG00-02 Inventory Growth Data & Account Access

Maintain a current matrix for:

- GitHub;
- OpenProject;
- website/deployment;
- booking/admin data;
- Google Ads;
- Google Business Profile;
- GA4;
- Search Console;
- social/content platforms when activated;
- finance/service outcome data required for economics.

**Current known:** Google Ads and GBP are connected through Windsor.ai; GA4 and Dr. Farah Search Console still require resolution.

**Gate:** `G0-CONTROL-PLANE-LIVE`

---

# Phase 1 — Stabilize Website, Booking and Production Operations

**Objective:** protect the core conversion path before increasing demand.

### P1.1 — Resolve/verify Brevo booking delivery incident

**State:** `IN_PROGRESS`  
**Workstream:** BG-10

Acceptance:

- production booking request persists;
- clinic/patient notification behavior matches the approved workflow;
- controlled receipt evidence exists;
- email failure cannot silently destroy the booking;
- no secret values are exposed in Git/chat/logs.

This is a HARD gate for meaningful paid traffic.

### P1.2 — Preserve accepted production/deployment controls

Do not restart completed migration work merely because old checklists exist.
Maintain:

- `dev` staging / `main` production separation;
- Jenkins-only deployment authority;
- environment/database/secret isolation;
- tested backup/restore controls;
- canonical production/staging domains;
- no routine direct commits to `main`;
- branch/PR discipline.

### P1.3 — Close remaining website operational inputs

Track and resolve where still current:

- final clinic factual/legal copy approvals;
- privacy/tracking copy after measurement design is implemented;
- staff MFA evidence where required;
- any unresolved production receipt evidence;
- approved imagery/video assets;
- high-resolution replacement assets where current quality is insufficient;
- any booking/admin usability defects discovered by marketing measurement.

### P1.4 — Maintain website conversion architecture

The website remains booking-first. Preserve/validate:

- prominent booking CTA;
- direct `/book` flow;
- click-to-call path;
- service-to-booking context;
- clear pending vs confirmed booking semantics;
- minimal collection of clinical information in marketing-facing flows;
- landing pages created only when supported by acquisition/search/business evidence.

**Gate:** `G1-BOOKING-HEALTHY`

---

# Phase 2 — Build the Measurement, Privacy and Attribution Foundation

**Objective:** optimize toward completed business outcomes, not superficial platform events.

### P2.1 — Complete production tag/measurement inventory

Known repository finding:

- no `gtag`, GTM, GA4 event layer or booking/call analytics implementation was found in inspected source;
- Google Ads account has Google tag `AW-17076731177` available;
- auto-tagging is enabled in Google Ads;
- current site implementation has not been validated as using that tag.

Complete runtime validation and document all production/staging trackers before implementation.

### P2.2 — Resolve GA4 access / property architecture

Required:

- identify/create the correct production GA4 property/data stream if needed;
- connect authorized access to the project analysis workflow;
- isolate staging from production;
- document measurement ID and ownership without exposing secrets;
- validate pageview/event receipt.

### P2.3 — Resolve Search Console access

Required:

- identify the correct production property for `drfarahvipurgentcare.com`;
- confirm ownership/verification;
- connect authorized access to the project workflow;
- validate sitemap/indexing reporting.

This task is also a dependency for BG30-04.

### P2.4 — BG00-03 Define canonical acquisition-source taxonomy

Canonical acquisition sources must distinguish at minimum:

- Google Ads;
- Google organic Search;
- Google Business/Maps where separately identifiable;
- direct;
- partner/referral;
- hotel/concierge;
- physician/surgery referral;
- social/content;
- other/unknown.

Preserve first-touch and useful last-non-direct/partner detail where technically appropriate.

### P2.5 — BG00-04 Define traveler/referral source capture

Separate:

- segment (`traveler yes/no/unknown`);
- acquisition source;
- source detail / partner identifier.

A traveler staying in a hotel is not automatically a hotel referral.

### P2.6 — Implement Google tag / GA4 architecture

Requirements:

- smallest non-duplicative implementation;
- production/staging isolation;
- source/campaign/partner preservation;
- support Google Ads attribution identifiers such as GCLID where applicable;
- no unnecessary patient clinical detail sent to marketing platforms;
- deploy through normal Git/Jenkins controls.

### P2.7 — Implement canonical conversion model

Use three layers rather than over-fragmenting optimization:

1. **diagnostic events** — site/funnel behavior;
2. **lead signal** — `booking_request_created` and qualified call signals;
3. **primary business outcome** — `visit_completed` once reliable linkage/import is validated.

`booking_request_created` must not be mislabeled as a confirmed visit.

### P2.8 — Implement `visit_completed` attribution/import

Target flow:

`ad/source identifier → booking/session linkage → appointment → status=completed → approved business-outcome event/import`

Requirements:

- opaque/internal linkage where possible;
- no unnecessary diagnosis/symptom/clinical narrative in marketing payload;
- deduplication/idempotency;
- timestamp/timezone integrity;
- defined correction behavior for status changes;
- end-to-end controlled test.

### P2.9 — Implement call/lead tracking where useful

Map to BG80-03. Distinguish:

- click-to-call;
- call;
- qualified call/contact where measurable;
- completed visit.

Do not treat every phone interaction as equivalent business value.

### P2.10 — Update privacy/cookie/tracking disclosures after architecture is final

Use the strongest useful lawful/platform-compliant measurement capability; do not impose arbitrary restrictions.

At the same time, align published privacy/cookie language with actual site behavior and applicable requirements.
The privacy page must no longer claim “essential cookies only / no third-party tracking” if the implemented stack contradicts that statement.

### P2.11 — End-to-end measurement validation

Validate a controlled journey from acquisition identifier through:

- landing page/session;
- booking request;
- appointment outcome;
- `visit_completed`;
- GA4 visibility;
- Google Ads conversion readiness/import;
- no duplicate firing;
- no unintended clinical data in marketing payloads.

**Gate:** `G2-MEASUREMENT-READY`

---

# Phase 3 — Capture Current Google and Search Baselines

This phase can proceed in parallel with Phase 1/2 where safe.

### P3.1 — BG20-01 Google Ads Forensic Audit

The former “pre-launch only” assumption is superseded.

**Verified historical fact:** the account contains paused Smart campaign `Urgent Care Medical Center` with activity from June 2025 through February 2026. Current live baseline documented in `docs/GOOGLE_ADS_BASELINE_2026-10-24.md` includes approximately:

- 258,541 impressions;
- 5,590 clicks;
- $4,494.86 spend;
- 16 platform-reported conversions.

Therefore BG20-01 is now a **historical forensic audit + relaunch-readiness audit**.

Preserve the original OpenProject children:

- `BG20-01.1` — Obtain Google Ads Access & Audit Window;
- `BG20-01.2` — Inventory Campaigns, Conversion Actions & Landing Pages;
- `BG20-01.3` — Analyze Search Terms, Keywords, Match Types & Negatives;
- `BG20-01.4` — Analyze Geography, Devices & Day/Hour Performance;
- `BG20-01.5` — Reconcile Google Ads to Qualified Contacts / Bookings / Completed Visits;
- `BG20-01.6` — Produce Google Ads Audit Findings & Decision Recommendations;
- `ADS-M1` — Google Ads Audit Decision-Ready.

Audit dimensions:

- account/campaign history;
- spend by period/campaign;
- conversion-action quality;
- Smart campaign legacy configuration;
- search terms/query intent where recoverable;
- geo/device/day-hour performance;
- landing destinations;
- automated rules;
- location assets/GBP linkage;
- healthcare policy exposure;
- relationship between platform conversions and actual completed visits.

### P3.2 — BG30-01 Google Business Profile Baseline

Preserve complete before-state before broad edits.

Live baseline already verifies:

- profile `Dr Farah VIP Urgent Care`;
- primary category `Urgent care center`;
- rating 5.0;
- 109 total reviews at the last live check;
- current profile service catalogue is extensive;
- Friday hours in the live profile were 8:30–16:30 while owner-confirmed regular hours were reported as 8:30–17:30 Monday–Friday.

Capture:

- ownership/verification;
- clinic/practitioner/duplicate structure;
- address/map pin;
- phone/site/booking links;
- categories;
- services;
- regular/special hours;
- service area;
- description;
- photos/video;
- reviews/replies;
- warnings/updates;
- performance/search keywords.

**Service-catalog rule:** do not remove services merely because the list is large. Evaluate factual availability, demand, economics, clarity, duplication, conversion usefulness, wording/pricing accuracy and Google policy before consolidating, rewriting, reprioritizing or removing anything.

### P3.3 — BG30-04 Search Console & Local SEO Baseline

After P2.3 access is resolved, audit:

- verification/property;
- sitemap;
- indexing;
- clicks/impressions/CTR;
- top queries/pages;
- branded vs non-branded demand;
- devices;
- urgent/pre-op/traveler/service themes;
- technical SEO handoffs.

### P3.4 — GA4 behavioral baseline

After P2.2/P2.6 are operational, establish baseline for:

- landing pages;
- traffic source/medium;
- booking funnel events;
- click-to-call;
- engagement by acquisition path;
- attribution quality/data gaps.

### P3.5 — BG30-05 Beverly Hills Local Search / Maps Competitor Baseline

Use controlled query/location methodology. Compare relevant competitors by:

- visibility;
- category;
- rating/review volume;
- hours;
- booking path;
- service messaging;
- website experience.

Do not claim one manual search equals universal ranking.

**Gate:** `G3-GOOGLE-BASELINES-CAPTURED`

---

# Phase 4 — Correct High-Confidence Foundation Problems

**Objective:** correct verified problems before major experimentation.

Priority order:

1. factual/policy/eligibility risk;
2. broken booking/tracking;
3. wrong public hours/contact/location/link;
4. conversion-goal misconfiguration;
5. duplicate profile or account hygiene risk;
6. service/category/public messaging issues;
7. landing-page/search-intent mismatch;
8. data-quality gaps.

### P4.1 — BG20-02 Implement Approved Google Ads Corrections

Possible corrections only after forensic audit:

- conversion goals/primary-secondary roles;
- campaign structure;
- geo/location options;
- scheduling;
- keywords/match types/negatives;
- assets/landing URLs;
- automated rules;
- GBP/location linkage;
- measurement/import configuration.

### P4.2 — BG30-02 Verify and Correct Core GBP Information

High-confidence factual corrections take priority.

Known candidate: verify and, if still correct, fix Friday closing time to the current approved clinic hours.

Do not perform broad service deletion. Use evidence-based service-catalog optimization.

### P4.3 — Technical SEO / website corrections

Route verified Search Console/GBP/Ads findings to BG-10:

- indexing/canonical/redirect issues;
- structured data;
- title/meta/content alignment;
- booking/CTA problems;
- landing page mismatch;
- tracking/source propagation;
- mobile/performance/accessibility issues that materially affect acquisition.

**Gate:** `G4-FOUNDATION-CORRECTED`

---

# Phase 5 — Establish Source, Service and Economic Decision Baselines

**Objective:** know which growth opportunities deserve investment.

### P5.1 — BG00-05 Establish Current Service & Revenue Baseline Request

Collect sufficient business-level data for service prioritization, including where available:

- completed visit count;
- collected revenue;
- variable/consumable cost;
- physician/staff time;
- capacity;
- repeat rate;
- referral leverage;
- acquisition source;
- cancellation/no-show burden.

### P5.2 — BG70-01 Evidence-Based Service Priority Matrix

Rank service lines using evidence, not enthusiasm alone:

- demand;
- revenue/contribution;
- capacity;
- clinical/operational fit;
- repeat potential;
- referral leverage;
- differentiation;
- acquisition cost;
- policy/compliance constraints.

The matrix governs which services receive sustained Google Ads, Local SEO, landing-page and content investment.

### P5.3 — BG00-06 Establish Growth Review & Decision Log Process

Adopt common decision vocabulary:

`SCALE / MODIFY / STOP / CONTINUE_MEASURING / MEASURE_FIRST / NO_ACTION`

### P5.4 — Establish source-completeness baseline

Measure how much of completed business can be assigned to a defensible acquisition/referral source.

**Gate:** `G5-ECONOMICS-AND-PRIORITIES-READY`

---

# Phase 6 — Build Evidence-Backed Landing Paths and Organic Foundations

**Objective:** acquisition intent must land on the right page with the right CTA and measurement.

### P6.1 — Prioritize landing-page needs

Candidate intent groups:

- urgent/same-day;
- brand;
- pre-op;
- traveler/VIP;
- selected high-priority services from BG70-01.

Create separate pages only when justified by demand, clarity, policy, SEO or campaign intent.

### P6.2 — Website handoff implementation

Each marketing → website handoff must include:

- evidence;
- affected URL/page;
- exact requirement;
- intended query/audience;
- approved claims;
- CTA;
- measurement requirement;
- primary KPI;
- acceptance evidence.

### P6.3 — Local/technical SEO implementation

Implement only evidence-backed changes from BG30-04/BG30-05.

### P6.4 — Review/testimonial website use

Use verified review excerpts only with appropriate authenticity/privacy/source handling. Preserve original meaning.

**Gate:** `G6-LANDING-PATHS-READY`

---

# Phase 7 — Relaunch and Optimize Paid Acquisition

### P7.1 — Design first controlled Google Ads experiment

Candidate campaign order is evidence-dependent, not fixed:

- Brand where protection/measurement justifies it;
- Urgent / Same-Day high-intent search;
- Pre-Op after landing/economics readiness;
- Traveler/Hotel only after operational readiness;
- sensitive services only after current policy review.

Define before launch:

- hypothesis;
- search intent/audience;
- geography;
- campaign/ad-group structure;
- keywords/match types;
- negatives;
- bidding;
- learning budget;
- landing page;
- primary/secondary conversions;
- `visit_completed` linkage plan;
- stop/modify/scale thresholds;
- decision date.

### P7.2 — Launch only after gates

Hard launch dependencies:

- `G1-BOOKING-HEALTHY`;
- `G2-MEASUREMENT-READY`;
- relevant `G4` corrections;
- relevant `G6` landing path readiness.

### P7.3 — BG20-03 Establish Paid Acquisition Optimization Cycle

Recurring review:

- spend;
- search terms;
- negatives;
- geo/device/day-hour;
- calls/bookings;
- completed visits;
- CAC where defensible;
- revenue/contribution where available;
- policy/disapproval changes.

**Gate:** `G7-FIRST-PAID-EXPERIMENT-LIVE`

---

# Phase 8 — Establish Google Business, Reputation and Local SEO Growth Cycle

Preserve BG-30 OpenProject work:

- `BG30-01` Google Business Profile Baseline;
- `BG30-02` Verify and Correct Core GBP Information;
- `BG30-03` Establish Review Acquisition & Response Workflow;
- `BG30-04` Search Console & Local SEO Baseline;
- `BG30-05` Beverly Hills Local Search / Maps Competitor Baseline;
- `REP-M1` Local Presence Baseline Complete.

### P8.1 — Review acquisition workflow

Use genuine, neutral review requests; no gating/fake reviews/incentivized five-star requests.

Track:

- new reviews/month;
- review request volume where available;
- rating;
- response rate/time;
- recurring reputation themes.

### P8.2 — Review response system

Responses remain privacy-safe and do not unnecessarily confirm treatment details.
Route serious clinical, billing, privacy or legal disputes appropriately.

### P8.3 — GBP optimization cycle

Optimize based on evidence:

- categories;
- services;
- hours/special hours;
- links;
- photos/video;
- description;
- posts where useful;
- search-keyword/performance data.

### P8.4 — Local SEO cycle

Use Search Console + GBP + competitor evidence to drive specific website changes and content priorities.

**Gate:** `G8-LOCAL-GROWTH-CYCLE-LIVE`

---

# Phase 9 — Hotel / Traveler / VIP Growth

Preserve the complete BG-40 OpenProject sequence:

- `BG40-01` Establish Traveler Patient Baseline;
- `BG40-02` Identify Existing Hotel / Concierge Referral Sources;
- `BG40-03` Build Priority Hotel / Concierge Target List;
- `BG40-04` Define Traveler / VIP Service Scope & Response Model;
- `BG40-05` Conduct Initial Hotel / Concierge Interviews;
- `BG40-06` Define Hotel Partner Kit Requirements;
- `BG40-07` Launch First Hotel / Concierge Partnership Pilot;
- `TRV-M1` Traveler Baseline Validated;
- `TRV-M2` First Hotel / Concierge Pilot Live.

Execution order:

1. measure current traveler volume/source/service/revenue/operational burden;
2. identify current/warm hotel/concierge sources;
3. define clinic/mobile/telehealth scope and response model;
4. conduct partner discovery interviews;
5. rank target partners;
6. define partner kit and attribution;
7. launch a small pilot;
8. evaluate completed visits, revenue, repeat referrals and operational reliability.

Dependencies:

- `BG90-03` hotel/mobile operational readiness & SLA;
- `BG90-04` physician/clinic capacity baseline;
- `BG90-05` referral-partnership compliance trigger;
- `BG90-06` marketing data privacy boundary;
- BG-80 attribution/source measurement.

Do not promise response times, mobile coverage or 24/7 availability until operationally approved.

---

# Phase 10 — Pre-Op Referral Engine

Preserve the complete BG-50 OpenProject sequence:

- `BG50-01` Establish Current Pre-Op Baseline;
- `BG50-02` Validate Pre-Op Referral Economics;
- `BG50-03` Define Pre-Op Referral Value Proposition;
- `BG50-04` Build Surgeon / Surgery-Center Target Database;
- `BG50-05` Create Pre-Op Referral Package;
- `BG50-06` Launch Initial Pre-Op Referral Outreach Pilot;
- `PREOP-M1` Pre-Op Referral Package Approved;
- `PREOP-M2` First Pre-Op Referral Pilot Live.

Execution order:

1. measure existing volume/source/revenue/turnaround/no-show;
2. quantify economics and capacity;
3. define referrer/patient value proposition;
4. map current/warm referrers;
5. build prioritized target list;
6. define referral package/workflow;
7. approve claims/turnaround/privacy/compliance;
8. run small outreach pilot;
9. measure active practices, referrals, completed clearances, repeat referrals, revenue and acquisition cost.

No referral compensation/per-patient arrangement without the appropriate BG90-05 compliance review trigger.

---

# Phase 11 — Physician-Led Video, Social and Creative System

Preserve BG-60 OpenProject work:

- `BG60-01` First Physician-Led Content Production Batch;
- `BG60-01.1` Define First Batch Audience, Goals & Content Pillars;
- `BG60-01.2` Prepare Filming Brief, Shot List & Asset Plan;
- `BG60-01.3` Prepare Scripts / Talking Points for Clinical Approval;
- `BG60-01.4` Produce First Professional Filming Session;
- `BG60-01.5` Organize Master Media Asset Library;
- `BG60-01.6` Edit Long-Form Physician Content;
- `BG60-01.7` Edit Short-Form Reels / Shorts / TikTok Assets;
- `BG60-01.8` Create Paid Social / Ad Creative Variants;
- `BG60-01.9` Create Website Video / Photography Derivatives;
- `BG60-01.10` Publish / Distribute Approved First Batch;
- `BG60-01.11` Review First-Batch Performance;
- `VID-M1` First Professional Content Batch Ready;
- `VID-M2` First Approved Content Batch Published;
- `BG60-02` Establish Ongoing Content Production & Distribution Cycle.

Content priorities should be fed by actual evidence from:

- Ads/search terms;
- Search Console;
- GBP/reviews;
- traveler interviews;
- pre-op referral questions;
- website/booking friction;
- BG70 service priorities.

Measure qualified traffic/booking assistance/business usefulness and reusable asset value, not views alone.

**Gate:** `G10-CONTENT-ENGINE-LIVE`

---

# Phase 12 — Analytics & Growth Intelligence

Preserve the known BG-80/OpenProject structure:

- `BG80-01` Instrument full conversion funnel;
- `BG80-02` Build growth dashboard & KPI reporting;
- `BG80-03` Implement call & lead tracking;
- `BG80-04` Establish attribution model;
- `BG80-05` Set up cohort & retention analytics;
- `BG80-06` Build experiment measurement framework;
- `BG80-07` Automate weekly growth report;
- `BG80-08` Integrate ChatGPT with OpenProject execution workflow;
- `EXP-GIP-001` Define Growth Intelligence MVP requirements;
- `GIP-M1` Growth analytics baseline live.

Where an older source called `BG80-01` “Define Minimum Attribution Model,” treat that as an earlier requirement concept now covered by the current BG80-01/BG80-04 structure; do not create a duplicate OpenProject item without verification.

### Technical sequence

1. stable acquisition/source taxonomy;
2. first-party session/source capture;
3. booking linkage via opaque internal reference;
4. confirmed/completed/cancelled/no-show outcome sync;
5. Google Ads cost ingestion (read-only initially);
6. referral/partner attribution;
7. revenue/business-outcome join where approved;
8. analytical views;
9. dashboard/KPI reporting;
10. experiment framework;
11. weekly automated report;
12. AI/Jupyter analysis on approved analytics views;
13. controlled external write automation only after later explicit approval.

The Growth Intelligence system is a business/marketing intelligence layer, not a second EHR.

**Gate:** `G11-GROWTH-INTELLIGENCE-BASELINE-LIVE`

---

# Phase 13 — Operations, Capacity, Privacy and Compliance Readiness

BG-90 is a cross-cutting dependency, not a final cleanup phase. Its tasks should run when triggered by the phases above.

Known required work packages from the former sources include:

- `BG90-03` Define Hotel / Mobile Care Operational Readiness & SLA / establish HIPAA-compliant marketing operations where applicable;
- `BG90-04` Establish Physician / Clinic Capacity Baseline;
- `BG90-05` Referral Partnership Compliance Review Trigger;
- `BG90-06` Establish Marketing Data Privacy Boundary.

Do not invent BG90-01/BG90-02 identifiers without OpenProject verification.

Trigger BG-90 review when work involves:

- public insurance/network claims;
- emergency/24-hour/same-day/mobile availability promises;
- sensitive healthcare advertising;
- referral compensation;
- review/privacy disputes;
- patient communication privacy;
- marketing/analytics data handling;
- service-area representations;
- scaling beyond clinic/physician capacity.

Privacy operating principle: use useful lawful/platform-compliant marketing measurement and attribution without unnecessary self-restriction, while excluding unnecessary medical-record detail and respecting required consent/privacy/platform rules.

---

# Phase 14 — Repeatable Growth Operating Cycle and Scaling

Once live acquisition/partner/content experiments exist, operate a recurring cadence.

### Weekly control review

- production booking/website health;
- Ads spend/search terms/conversion quality;
- GBP/review changes;
- GA4/attribution data quality;
- source coverage;
- experiment blockers;
- urgent operational/compliance risks.

### Monthly business review

- completed visits by source/service;
- defensible CAC;
- collected revenue/contribution where available;
- local/organic performance;
- partner/referral production;
- service economics;
- capacity;
- retention/repeat/referral;
- experiment decisions.

### Scale rule

No channel is scaled solely because clicks, leads, views or platform conversions increased.
Scaling should be supported by completed visits, acceptable economics, capacity and measurement confidence.

**Gate:** `G12-REPEATABLE-GROWTH-CYCLE`

---

## 6. Exact OpenProject work-package inventory preserved from former tabs

### BG-00

- `BG00-01` Validate OpenProject Project Access & Membership
- `BG00-02` Inventory Growth Data & Account Access
- `BG00-03` Define Canonical Patient Acquisition-Source Taxonomy
- `BG00-04` Define Traveler / Referral Source Capture
- `BG00-05` Establish Current Service & Revenue Baseline Request
- `BG00-06` Establish Growth Review & Decision Log Process
- `M0` Growth Execution System Live
- `M1` Measurement Baseline Established
- `M2` First Growth Experiments Live
- `M3` First Performance Decision Review
- `M4` Repeatable Growth Operating Cycle Established

### BG-20

- `BG20-01` Google Ads Forensic Audit
- `BG20-01.1` Obtain Google Ads Access & Audit Window
- `BG20-01.2` Inventory Campaigns, Conversion Actions & Landing Pages
- `BG20-01.3` Analyze Search Terms, Keywords, Match Types & Negatives
- `BG20-01.4` Analyze Geography, Devices & Day/Hour Performance
- `BG20-01.5` Reconcile Google Ads to Qualified Contacts / Bookings / Completed Visits
- `BG20-01.6` Produce Google Ads Audit Findings & Decision Recommendations
- `ADS-M1` Google Ads Audit Decision-Ready
- `BG20-02` Implement Approved Google Ads Corrections
- `BG20-03` Establish Paid Acquisition Optimization Cycle

### BG-30

- `BG30-01` Google Business Profile Baseline
- `BG30-02` Verify and Correct Core Google Business Profile Information
- `BG30-03` Establish Review Acquisition & Response Workflow
- `BG30-04` Search Console & Local SEO Baseline
- `BG30-05` Beverly Hills Local Search / Maps Competitor Baseline
- `REP-M1` Local Presence Baseline Complete

### BG-40

- `BG40-01` Establish Traveler Patient Baseline
- `BG40-02` Identify Existing Hotel / Concierge Referral Sources
- `BG40-03` Build Priority Hotel / Concierge Target List
- `BG40-04` Define Traveler / VIP Service Scope & Response Model
- `BG40-05` Conduct Initial Hotel / Concierge Interviews
- `BG40-06` Define Hotel Partner Kit Requirements
- `BG40-07` Launch First Hotel / Concierge Partnership Pilot
- `TRV-M1` Traveler Baseline Validated
- `TRV-M2` First Hotel / Concierge Pilot Live

### BG-50

- `BG50-01` Establish Current Pre-Op Baseline
- `BG50-02` Validate Pre-Op Referral Economics
- `BG50-03` Define Pre-Op Referral Value Proposition
- `BG50-04` Build Surgeon / Surgery-Center Target Database
- `BG50-05` Create Pre-Op Referral Package
- `BG50-06` Launch Initial Pre-Op Referral Outreach Pilot
- `PREOP-M1` Pre-Op Referral Package Approved
- `PREOP-M2` First Pre-Op Referral Pilot Live

### BG-60

- `BG60-01` First Physician-Led Content Production Batch
- `BG60-01.1` Define First Batch Audience, Goals & Content Pillars
- `BG60-01.2` Prepare Filming Brief, Shot List & Asset Plan
- `BG60-01.3` Prepare Scripts / Talking Points for Clinical Approval
- `BG60-01.4` Produce First Professional Filming Session
- `BG60-01.5` Organize Master Media Asset Library
- `BG60-01.6` Edit Long-Form Physician Content
- `BG60-01.7` Edit Short-Form Reels / Shorts / TikTok Assets
- `BG60-01.8` Create Paid Social / Ad Creative Variants
- `BG60-01.9` Create Website Video / Photography Derivatives
- `BG60-01.10` Publish / Distribute Approved First Batch
- `BG60-01.11` Review First-Batch Performance
- `VID-M1` First Professional Content Batch Ready
- `VID-M2` First Approved Content Batch Published
- `BG60-02` Establish Ongoing Content Production & Distribution Cycle

### BG-70

- `BG70-01` Evidence-Based Service Priority Matrix

Only this exact identifier was recoverable from the consolidated source set. Do not fabricate additional BG-70 OpenProject codes; add them only when verified in OpenProject.

### BG-80

- `BG80-01` Instrument full conversion funnel
- `BG80-02` Build growth dashboard & KPI reporting
- `BG80-03` Implement call & lead tracking
- `BG80-04` Establish attribution model
- `BG80-05` Set up cohort & retention analytics
- `BG80-06` Build experiment measurement framework
- `BG80-07` Automate weekly growth report
- `BG80-08` Integrate ChatGPT with OpenProject execution workflow
- `EXP-GIP-001` Define Growth Intelligence MVP requirements
- `GIP-M1` Growth analytics baseline live

### BG-90

Verified identifiers recovered from the former sources:

- `BG90-03` Define Hotel / Mobile Care Operational Readiness & SLA / marketing-operations readiness dependency
- `BG90-04` Establish Physician / Clinic Capacity Baseline
- `BG90-05` Referral Partnership Compliance Review Trigger
- `BG90-06` Establish Marketing Data Privacy Boundary

Do not invent missing BG90 identifiers until verified against OpenProject.

### BG-10 / website work

The repository itself is the detailed technical source for BG-10. Do not invent OpenProject numeric child codes from memory. The roadmap preserves these durable website obligations:

- booking/email reliability;
- production/staging/deployment integrity;
- admin/booking operational usability;
- technical SEO and redirect/indexing quality;
- measurement/tag implementation;
- source/UTM/partner attribution propagation;
- conversion-focused landing pages;
- privacy/tracking copy alignment;
- approved legal/factual content;
- website media/creative derivatives;
- performance/accessibility/conversion issues when evidence shows business impact.

When exact BG-10 OpenProject identifiers are needed, verify them in OpenProject and add the mapping to `PROJECT_HANDOFF.md` or this inventory.

---

## 7. Current priority queue — 2026-10-24

This queue is a snapshot. `PROJECT_HANDOFF.md` is the live resume point and must be updated after every material session.

| Priority | Item | Current state | Dependency / next evidence |
|---:|---|---|---|
| 0 | Replace Project Sources with minimal `dev` routers and run resume test | IN_PROGRESS | P0.1 complete; upload replacement files, then verify BG-20 can resume from GitHub alone |
| 1 | Resolve/verify production booking/Brevo delivery | IN_PROGRESS | controlled production booking + expected notification evidence |
| 2 | Resolve Dr. Farah GA4 access/property | READY | correct property/data stream + connection + runtime test |
| 3 | Resolve Dr. Farah Search Console property/access | READY | production property + verification + connection |
| 4 | Finalize measurement/privacy architecture | IN_PROGRESS | tag inventory + GA4 + source capture + privacy design |
| 5 | Implement/test Google tag + GA4 + source/GCLID persistence | WAITING on P2 design/access | code + deployment + live validation |
| 6 | Implement/test `visit_completed` business-outcome attribution | READY FOR DESIGN / implementation after linkage | appointment outcome linkage + import validation |
| 7 | Complete Google Ads historical forensic audit | IN_PROGRESS | live Ads evidence; reconcile platform conversions to outcomes |
| 8 | Complete GBP baseline and high-confidence corrections | IN_PROGRESS | baseline preserved; verify Friday hours before write |
| 9 | Run Search Console/local competitor/organic baseline | WAITING on access | P2.3 |
| 10 | Establish service/revenue/source baseline and BG70 matrix | READY in parallel | business records/data request |
| 11 | Implement evidence-backed landing/local SEO changes | NOT_STARTED | findings from phases 3–6 |
| 12 | Launch first controlled Ads relaunch | BLOCKED | G1 + G2 + applicable G4/G6 |
| 13 | Establish review/reputation cycle | READY after GBP baseline | BG30-03 |
| 14 | Traveler baseline / hotel-source map | READY in parallel when data available | BG40-01/02 + source taxonomy |
| 15 | Pre-op baseline/economics | READY in parallel when data available | BG50-01/02 + business data |
| 16 | First physician-led content architecture | PAUSED until near-term priorities clearer | use Ads/SC/GBP/service evidence |
| 17 | Growth Intelligence MVP beyond core attribution | DEFERRED until source/outcome contract stable | EXP-GIP-001 gate |

---

## 8. Safe parallel work matrix

While booking/Brevo is unresolved, the following may safely proceed:

- Google Ads read-only forensic analysis;
- GBP baseline/reputation analysis;
- GA4/Search Console access work;
- measurement design;
- Search/local competitor research;
- source taxonomy;
- service/revenue baseline request;
- traveler/pre-op historical baseline reconstruction;
- content research/briefing that does not publish unsupported claims.

Do **not** start meaningful paid traffic while booking/measurement hard gates remain red.

---

## 9. Roadmap maintenance rules

1. This is the only master sequencing document.
2. A detailed runbook/specification may describe *how* to perform work but may not silently become a competing roadmap.
3. New work enters this roadmap only when it is material, durable and not already represented by a workstream item.
4. Do not duplicate OpenProject children merely to mirror every checklist line.
5. When an OpenProject identifier is unknown, do not invent it.
6. When a workstream plan changes, preserve the old intent/history in Git rather than deleting evidence without explanation.
7. `PROJECT_HANDOFF.md` always contains the exact current resume point; this roadmap contains the durable order/gates.
8. A future ChatGPT session should be able to resume by reading GitHub without reading old chats.

---

## 10. Minimum resume protocol for any future session

Read in this order:

1. `README.md`;
2. `PROJECT_HANDOFF.md`;
3. this `ROADMAP.md` current-priority and relevant phase;
4. `docs/DECISIONS.md` if approval/strategy is involved;
5. the relevant dated baseline/spec/runbook;
6. current live account/system when state may have changed;
7. OpenProject only when current work-package execution metadata matters.

Then:

- re-check blockers;
- select highest eligible task;
- execute/validate;
- update GitHub before ending.

This protocol is mandatory for continuity across chat context resets, future tabs, future operators and long gaps between sessions.
