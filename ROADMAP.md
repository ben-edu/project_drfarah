# Dr. Farah VIP Urgent Care — Master Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Canonical roadmap:** this file only  
> **Integration branch:** `dev`  
> **Production branch:** `main`  
> **GitHub:** durable project memory, code, roadmap, handoff, decisions and evidence  
> **OpenProject:** authoritative for live work-package status, assignee, dates, dependencies and milestones  
> **Live systems:** authoritative for their own current state

**Operating mode updated 2026-10-28:** Growth Acceleration / parallel execution.

---

## 1. Mission

The project is not only a website or measurement implementation. The operating objective is to build and run an integrated growth system that coordinates:

- Google Ads and paid acquisition;
- Google Search Console / organic search;
- Google Business Profile / Maps / reputation;
- GA4 and privacy-safe measurement;
- first-party attribution and completed-visit conversion feedback;
- conversion-focused website and landing paths;
- service economics, capacity and budget decisions;
- AI/ChatGPT advertising where eligible and economically justified;
- traveler/hotel, pre-op referral and physician-led content channels;
- Growth Intelligence, reporting and recurring optimization.

The system must optimize toward business outcomes, especially completed visits and defensible economics, rather than clicks, views or platform-reported conversions alone.

---

## 2. Authority and control

When sources disagree, use this order:

1. current verified clinic/business fact from Dr. Farah or authoritative clinic record;
2. live production/account system for its own state;
3. approved `docs/DECISIONS.md`;
4. current `PROJECT_HANDOFF.md` + this roadmap;
5. stable repository specifications/runbooks/code;
6. OpenProject for live execution metadata;
7. historical reports/old project sources/chats.

Special authorities:

- website/deployment → GitHub + Jenkins + live environment;
- Google Ads → live Google Ads account;
- GBP → live verified profile;
- organic search → Search Console + live site;
- GA4 → live GA4 property/data stream;
- completed visit → booking/admin platform;
- work-package metadata → OpenProject.

`PROJECT_HANDOFF.md` is the exact live resume point and must be updated after every material session.

---

## 3. Execution rules — Growth Acceleration mode

1. **Parallel by default.** Independent workstreams proceed simultaneously; a blocker in one lane does not stop safe work in another.
2. **Production is the destination.** Growth infrastructure that passes staging/quality gates must not remain indefinitely on `dev`. Promote coherent batches through normal Jenkins controls.
3. **Develop more, build less.** Batch related changes, tests and docs before CI/build. Do not trigger redundant builds, but never trade away correctness or safety.
4. **One integrated measurement model.** Google Ads, Search Console, GBP, GA4, first-party attribution and the website must be designed as one acquisition system.
5. **Legacy evidence before cleanup.** Historical campaigns/settings may be archived or removed only after extracting useful performance/configuration evidence. Do not destroy forensic value first.
6. **Do not relaunch the legacy Smart campaign by default.** The first new paid experiment should use a controllable campaign architecture unless live evidence demonstrates a better alternative.
7. **Working assumptions are allowed.** Missing exact clinic economics must not stall research/design. Use clearly labeled provisional assumptions derived from market/account evidence, then replace them when authoritative business figures become available.
8. **Completed visit is the primary business outcome.** Booking/call signals may remain secondary/diagnostic.
9. **Privacy boundary.** Do not send unnecessary patient PII/PHI, reason for visit, service/clinical context or registration data to marketing platforms.
10. **AI paid acquisition is a real workstream.** ChatGPT/OpenAI Ads eligibility, policy, targeting, measurement and economics are to be evaluated as a potential paid channel, not left as a side note.

---

## 4. Master gates

| Gate | Meaning | Minimum evidence |
|---|---|---|
| `G0-CONTROL-PLANE-LIVE` | GitHub can carry continuity | roadmap + handoff + decisions + resume protocol |
| `G1-BOOKING-HEALTHY` | production booking is operationally safe | booking persists + notification behavior verified |
| `G2-MEASUREMENT-READY` | acquisition can be measured to business outcome | production attribution + completed-visit import path tested without duplicate/bad data |
| `G3-GOOGLE-BASELINES-CAPTURED` | current Ads/GBP/SC/GA4 state is known | dated live evidence |
| `G4-FOUNDATION-CORRECTED` | verified high-confidence issues corrected | before/after evidence |
| `G5-ECONOMICS-AND-PRIORITIES-READY` | services/budget can be judged economically | service/source baseline or defensible provisional model |
| `G6-LANDING-PATHS-READY` | paid intent lands on appropriate page/CTA | page + message + tracking acceptance |
| `G7-FIRST-PAID-EXPERIMENT-LIVE` | controlled paid experiment is spending | campaign spec + budget + measurement + stop/scale rules |
| `G8-LOCAL-GROWTH-CYCLE-LIVE` | GBP/reputation/local SEO has recurring operating cycle | workflow + baseline + cadence |
| `G9-AI-PAID-EXPERIMENT-READY` | AI advertising can be tested responsibly | eligibility + campaign hypothesis + measurement + budget/stop rules |
| `G10-PARTNERSHIP-EXPERIMENTS-LIVE` | traveler/pre-op pilots running | operational/compliance + attribution + pilot spec |
| `G11-CONTENT-ENGINE-LIVE` | reusable physician-led content system live | first batch published/measured |
| `G12-GROWTH-INTELLIGENCE-LIVE` | source→completed-visit reporting operational | joins + quality checks + reporting |
| `G13-REPEATABLE-GROWTH-CYCLE` | scale/modify/stop cadence is routine | recurring reviews tied to outcomes/economics |

Current gate state on 2026-10-28:

- `G1-BOOKING-HEALTHY`: GREEN unless new regression appears.
- `G2-MEASUREMENT-READY`: RED / IN_PROGRESS.
- `G3-GOOGLE-BASELINES-CAPTURED`: PARTIAL; Ads/GBP/Search Console baselines exist, GA4 live receipt still needs confirmation.
- downstream paid-scale gates remain unearned.

---

# Phase A — Immediate Production Measurement Completion

**Objective:** move the already-built measurement stack from development to verified production as one coherent batch.

### A1 — Validate current `dev` runtime

Current `dev` head: `c976a56836ca4160684be2b190d6aa29e7244032`; Jenkins `dev/24` is green.

Validate, without unnecessary new application builds where possible:

- service-account credential readability and ADC auth;
- Google Data Manager API reachability;
- destination/customer/conversion-action acceptance in `validateOnly` mode;
- no click-ID or patient-data leakage to logs/errors;
- attribution persistence and `visit_completed` construction.

### A2 — Promote coherent measurement batch to `main`

After A1 passes, promote the complete compatible batch rather than leaving it on `dev`:

- Google Data Manager payload preparation;
- guarded Data Manager client;
- credential mount/readiness behavior;
- any required documentation/runbook changes.

Production deployment must remain Jenkins-controlled.

### A3 — Production smoke validation

Verify on production:

- real landing URL with safe test campaign parameters preserves attribution to booking;
- production booking remains healthy;
- selected-page GA4 behavior matches approved privacy architecture;
- excluded sensitive pages do not receive unintended analytics measurement;
- conversion import remains guarded until controlled recording approval.

### A4 — First controlled completed-visit import

When one legitimate completed appointment has an eligible real Google click ID:

1. validate the exact real row with recording disabled;
2. send one controlled `visit_completed` conversion with explicit recording authorization;
3. verify dedupe/idempotency by replaying the same transaction ID safely;
4. reconcile Google Ads against the internal completed appointment;
5. keep the conversion action Secondary until the end-to-end path is trusted.

**Gate:** `G2-MEASUREMENT-READY`.

---

# Phase B — Google Ads Forensics, Cleanup and New Campaign Architecture

This phase proceeds in parallel with Phase A.

### B1 — Preserve/extract legacy campaign evidence before deletion

Historical Smart campaign: `Urgent Care Medical Center`, paused, June 2025–February 2026, approximately 258,541 impressions, 5,590 clicks, $4,494.86 spend and 16 platform-reported conversions.

Extract all useful recoverable evidence before archive/deletion decisions:

- search/query themes where available;
- geography;
- device;
- day/hour;
- landing destinations;
- ad/creative/message history;
- conversion actions and goal configuration;
- location assets/GBP linkage;
- automated settings/rules;
- spend and outcome trends;
- policy/disapproval history where available.

Do not assume platform conversions equal completed visits.

### B2 — Decide legacy cleanup

After B1:

- keep only objects that still provide useful history/reference or are needed for account integrity;
- pause/archive/remove obsolete assets/settings when safe;
- do not reactivate the old Smart campaign as the primary relaunch vehicle by default.

### B3 — Build the new first Google Ads campaign architecture

Default hypothesis: tightly controlled Search campaign(s), not Smart, subject to live account/policy evidence.

Before launch define:

- high-intent service/query clusters;
- campaign/ad-group structure;
- exact/phrase/broad-match role based on data and bidding maturity;
- comprehensive negative-keyword system;
- Beverly Hills / relevant service-area geography and location option settings;
- device/day-hour logic;
- ad copy and assets;
- landing page per intent cluster;
- primary/secondary conversion roles;
- bidding strategy appropriate to conversion-volume maturity;
- learning budget;
- stop / modify / scale thresholds.

### B4 — Keyword and demand research

Use together:

- historical Google Ads evidence;
- Google Search Console query data;
- current Keyword Planner/live Google Ads planning data where available;
- local competitor/query evidence;
- service economics and capacity;
- landing-page relevance.

The objective is not the largest keyword list. It is maximum useful intent coverage with controlled waste.

### B5 — Pilot budget model

Until exact clinic economics are supplied, use provisional assumptions clearly labeled as such. Build the pilot budget from:

- forecast CPC/query volume;
- expected click→booking rate range;
- expected booking→completed-visit rate range;
- plausible completed-visit contribution range;
- minimum sample needed to make a decision;
- hard spend ceiling and early-stop triggers.

Replace assumptions with authoritative clinic revenue/cost/capacity data when available; do not block campaign design waiting for perfect figures.

**Gate:** `G5` + `G6` → `G7-FIRST-PAID-EXPERIMENT-LIVE`.

---

# Phase C — Google Search Console, SEO and Landing-Page Growth

Proceed in parallel with A/B.

Current Search Console property: `sc-domain:drfarahvipurgentcare.com`.

Recent live 90-day baseline captured on 2026-10-28: approximately 32.3K impressions, 308 clicks, CTR ~0.95%, average position ~11.8.

### C1 — Query opportunity map

Prioritize:

- high-intent local urgent-care queries near positions 4–20;
- brand queries needing protection/clarity;
- Beverly Hills / near-me themes;
- commercially relevant service queries;
- pre-op/traveler/VIP opportunities;
- weak or irrelevant query clusters that should not drive paid spend.

### C2 — Technical/indexing review

Continue verified fixes for:

- sitemap/indexing;
- canonical/redirect behavior;
- title/meta/content alignment;
- schema/structured data where justified;
- mobile/performance/accessibility issues with acquisition impact.

`/book` and `/patient-registration` remain `noindex` and excluded from sitemap unless strategy changes explicitly.

### C3 — Paid/organic landing map

For each priority intent, decide whether to:

- improve an existing page;
- create a dedicated landing page;
- route to a current service page;
- avoid targeting until content/operational readiness exists.

Each page must have one intended audience, primary CTA, tracking plan and acceptance metric.

**Gate:** `G6-LANDING-PATHS-READY`.

---

# Phase D — Google Business Profile, Maps and Reputation Optimization

Current profile: Dr Farah VIP Urgent Care; primary category `Urgent care center`; baseline rating 5.0 / 109 reviews at captured baseline.

Recent 90-day live data captured 2026-10-28: approximately 120 website clicks and 123 call clicks.

### D1 — Core factual accuracy

Validate and correct:

- regular/special hours;
- address/map pin;
- phone;
- website/booking links;
- primary/secondary categories;
- service-area representation.

### D2 — Service-catalog optimization

Do not bulk-delete merely because the catalogue is large. Evaluate each relevant service for:

- factual availability;
- demand;
- economics;
- clarity/duplication;
- strategic priority;
- website/landing alignment;
- claims/pricing accuracy;
- Google policy.

### D3 — Reputation operating system

Establish privacy-safe workflow for:

- genuine neutral review requests;
- response cadence;
- response templates/guardrails;
- issue escalation;
- review-theme analysis feeding website/Ads/content.

### D4 — Maps/local competitor loop

Track relevant Beverly Hills competitors by visibility, category, reviews, hours, messaging and booking experience; use the evidence to improve GBP/site/Ads, not to copy blindly.

**Gate:** `G8-LOCAL-GROWTH-CYCLE-LIVE`.

---

# Phase E — GA4 and Cross-Channel Measurement Quality

GA4 production property: `489069776`; Web Stream `11211773871`; Measurement ID `G-D58FTMF05S`.

### E1 — Confirm live data receipt/settings

Verify:

- Realtime/DebugView safe controlled event;
- timezone/currency;
- Enhanced Measurement settings;
- selected-page allowlist behavior;
- consent behavior;
- no unintended page/query/title/referrer/clinical leakage.

### E2 — Keep roles clear

- GA4 = behavioral/diagnostic analysis on approved low-risk surfaces;
- first-party database = source/click→appointment linkage;
- Google Ads offline conversion = advertising optimization feedback;
- Search Console = organic Google search truth;
- GBP = Maps/profile truth.

Do not duplicate measurement simply because multiple Google tools can collect something similar.

---

# Phase F — First Paid Experiment and Optimization Cycle

Launch only when booking is healthy, the relevant landing path is ready and the completed-visit feedback path is sufficiently trusted.

### F1 — Controlled launch

The first experiment must have:

- named hypothesis;
- exact target intent/geography;
- finite learning budget;
- controlled keywords/match types/negatives;
- relevant landing page;
- `Visit Completed` business-outcome linkage;
- secondary booking/call diagnostics;
- stop/modify/scale thresholds;
- review date.

### F2 — Search-term waste control

Early review cadence must aggressively identify irrelevant intent and add negatives before scaling.

### F3 — Scale only on business evidence

No channel is scaled only because CTR, clicks, leads or platform conversions increased. Prefer completed visits, defensible CAC/contribution, capacity and measurement confidence.

**Gate:** `G7-FIRST-PAID-EXPERIMENT-LIVE`.

---

# Phase G — Stable Offline Conversion Operations

After the first controlled real conversion succeeds, convert the manual path into a durable background process.

Required behavior:

- identify eligible new `visit_completed` rows with click IDs;
- record import state/idempotency;
- batch safely;
- retry transient failures with bounded backoff;
- quarantine permanent/schema/auth failures;
- never print click IDs or patient data in routine logs;
- expose health/metrics without sensitive payloads;
- alert on sustained failures;
- reconcile imports to Google Ads periodically.

This is operational automation, not autonomous marketing spend.

---

# Phase H — AI / ChatGPT Ads Paid Channel

Treat this as a current growth workstream.

### H1 — Eligibility and policy verification

Verify current account/healthcare eligibility and applicable policy before spend. Do not assume access or approval.

### H2 — Channel hypothesis

If eligible, determine where ChatGPT Ads can add incremental value versus Google Search, including:

- high-intent local care discovery;
- traveler/VIP use cases;
- pre-op/referral-adjacent discovery where policy permits;
- brand/context discovery.

### H3 — Measurement and landing path

Use dedicated source/UTM/partner-style attribution and the same completed-visit business outcome where technically and policy-compliantly possible.

### H4 — Controlled pilot

Create a finite-budget pilot with explicit stop/scale rules. Do not treat AI advertising as profitable merely because it is new.

**Gate:** `G9-AI-PAID-EXPERIMENT-READY`.

---

# Phase I — Service Economics and Capacity

Work in parallel; do not wait for perfect accounting.

For each priority service estimate/collect:

- completed visit count;
- collected revenue;
- variable/consumable cost;
- physician/staff time;
- capacity;
- repeat/referral leverage;
- no-show/cancellation burden;
- acquisition cost;
- policy/operational constraints.

Rank services by demand × contribution × capacity × differentiation × acquisition efficiency × strategic value.

**Gate:** `G5-ECONOMICS-AND-PRIORITIES-READY`.

---

# Phase J — Traveler / Hotel / VIP Growth

Preserve sequence:

- traveler baseline;
- existing hotel/concierge sources;
- target list;
- service scope/response model;
- partner interviews;
- partner kit;
- attribution;
- small pilot;
- completed-visit/revenue/repeat-referral review.

No unsupported 24/7, mobile or response-time promise.

---

# Phase K — Pre-Op Referral Engine

Preserve sequence:

- current baseline;
- economics/capacity;
- value proposition;
- current/warm referrer map;
- target surgeons/surgery centers;
- referral package/workflow;
- claims/privacy/compliance review;
- small outreach pilot;
- completed clearance/repeat-referral/revenue review.

No per-patient/referral compensation arrangement without appropriate compliance review.

---

# Phase L — Physician-Led Content / Creative

Content priorities must be fed by Search Console, Ads search terms, GBP/reviews, traveler/pre-op questions, website friction and service economics.

Build reusable long-form + short-form + website + paid creative derivatives. Measure qualified business contribution, not views alone.

---

# Phase M — Growth Intelligence and Recurring Operating Cycle

Technical/business sequence:

1. stable source taxonomy;
2. source/session capture;
3. booking linkage;
4. completed/cancelled/no-show outcomes;
5. Ads cost;
6. GBP/Search/GA4 signals;
7. referral/partner attribution;
8. revenue/contribution where approved;
9. analytical views/dashboard;
10. experiment framework;
11. weekly growth report;
12. recurring SCALE / MODIFY / STOP / CONTINUE_MEASURING decisions.

The Growth Intelligence layer is not an EHR and must not become one.

**Gate:** `G12-GROWTH-INTELLIGENCE-LIVE` → `G13-REPEATABLE-GROWTH-CYCLE`.

---

## 6. Preserved OpenProject work-package identifiers

### BG-00
`BG00-01`, `BG00-02`, `BG00-03`, `BG00-04`, `BG00-05`, `BG00-06`, `M0`, `M1`, `M2`, `M3`, `M4`.

### BG-20
`BG20-01`, `BG20-01.1`, `BG20-01.2`, `BG20-01.3`, `BG20-01.4`, `BG20-01.5`, `BG20-01.6`, `ADS-M1`, `BG20-02`, `BG20-03`.

### BG-30
`BG30-01`, `BG30-02`, `BG30-03`, `BG30-04`, `BG30-05`, `REP-M1`.

### BG-40
`BG40-01`, `BG40-02`, `BG40-03`, `BG40-04`, `BG40-05`, `BG40-06`, `BG40-07`, `TRV-M1`, `TRV-M2`.

### BG-50
`BG50-01`, `BG50-02`, `BG50-03`, `BG50-04`, `BG50-05`, `BG50-06`, `PREOP-M1`, `PREOP-M2`.

### BG-60
`BG60-01`, `BG60-01.1`, `BG60-01.2`, `BG60-01.3`, `BG60-01.4`, `BG60-01.5`, `BG60-01.6`, `BG60-01.7`, `BG60-01.8`, `BG60-01.9`, `BG60-01.10`, `BG60-01.11`, `VID-M1`, `VID-M2`, `BG60-02`.

### BG-70
`BG70-01` only is verified. Do not fabricate additional codes.

### BG-80
`BG80-01`, `BG80-02`, `BG80-03`, `BG80-04`, `BG80-05`, `BG80-06`, `BG80-07`, `BG80-08`, `EXP-GIP-001`, `GIP-M1`.

### BG-90
Verified: `BG90-03`, `BG90-04`, `BG90-05`, `BG90-06`. Do not invent missing identifiers.

BG-10 exact child identifiers must be verified from OpenProject when needed; repository remains the detailed technical source.

---

## 7. Current parallel priority queue — 2026-10-28

| Priority | Lane | Item | State / next evidence |
|---:|---|---|---|
| 0 | Production measurement | Validate Data Manager auth/destination using current green `dev` artifact, then prepare one coherent `main` promotion | IN_PROGRESS |
| 1 | Production measurement | Production attribution/GA4/booking smoke validation after promotion | READY after P0 |
| 2 | Google Ads | Extract legacy Smart-campaign forensic value before cleanup | IN_PROGRESS |
| 3 | Google Ads | Build new Search campaign architecture, keyword/negative/geo/ad/landing/budget spec | READY NOW |
| 4 | Search/website | Build Search Console opportunity + landing-page map | READY NOW |
| 5 | GBP/local | Audit/correct core GBP + service/reputation/local strategy | READY NOW |
| 6 | GA4 | Confirm live receipt/settings and close behavioral baseline gap | IN_PROGRESS |
| 7 | Economics | Create provisional service/economics model; replace assumptions as clinic figures arrive | READY NOW |
| 8 | Paid pilot | Create paused/ready campaign and launch spec; spend only after relevant gates | READY for design |
| 9 | Real conversion | First legitimate click→booking→completed visit→Google Ads import | WAITING for eligible real event after campaign traffic exists |
| 10 | Conversion operations | Add durable import ledger/scheduler/retry/monitoring after controlled real import | READY for design; recording activation waits on #9 |
| 11 | AI Ads | Verify current eligibility/policy and design channel pilot | READY NOW |
| 12 | Local/reputation | Establish recurring review/GBP/Maps cycle | READY NOW |
| 13 | Traveler/pre-op/content | Advance independent research/baselines in parallel | READY where inputs exist |
| 14 | Growth Intelligence | Cross-channel dashboard/weekly decision loop | follows stable source/outcome data but design may proceed |

---

## 8. What must not block progress

Do not stop all growth work because:

- one API validation is waiting;
- exact clinic margin is not yet available;
- the first real paid conversion has not happened yet;
- one Google tool has an access/reporting gap;
- an AI ad channel is awaiting eligibility review.

Instead, document the blocker, preserve the restart condition and continue the highest-value independent lane.

---

## 9. What must still block spend/scale

Do not materially scale paid traffic when any of these are true:

- production booking is unhealthy;
- attribution is known broken;
- landing intent is materially mismatched;
- conversion recording is duplicating/corrupting outcomes;
- campaign economics are clearly unacceptable;
- policy/eligibility forbids the planned targeting/creative;
- clinic capacity cannot absorb the expected demand.

A small controlled learning experiment may proceed once its own minimum safety/measurement dependencies are satisfied; scale requires stronger evidence.

---

## 10. Resume protocol

Every substantive session:

1. read `PROJECT_HANDOFF.md`;
2. read this current priority queue and relevant lane;
3. check live systems for facts that may have changed;
4. re-check HARD blockers;
5. execute the highest-value eligible work in parallel lanes;
6. batch related code changes before CI/build;
7. record material evidence/results in GitHub;
8. update `PROJECT_HANDOFF.md` before ending.

No material project result should exist only in chat.
