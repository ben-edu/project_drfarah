# Dr. Farah VIP Urgent Care — Master Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Integration branch:** `dev`  
> **Production branch:** `main`  
> **Live systems:** authoritative for their own current state  
> **Handoff:** `PROJECT_HANDOFF.md` is the exact resume point

**Operating mode:** Growth Acceleration / parallel execution.  
**Roadmap refreshed:** 2026-10-29.

## Mission and execution rules

Build one integrated growth system across Google Ads, Search Console, GBP, GA4, first-party attribution, completed-visit feedback, conversion-focused landing paths, economics, ChatGPT Ads, referral/partner channels and Growth Intelligence. Optimize toward completed visits and defensible economics.

Parallelize safe work. Promote validated work to production promptly. Batch related development before CI. Preserve legacy evidence before cleanup. Use explicit provisional economics rather than waiting for perfect inputs. Keep privacy boundaries strict: no unnecessary patient PII/PHI, reason-for-visit or clinical context in marketing platforms. Tests that require real campaign traffic belong inside the controlled pilot; only production, privacy/security, data-integrity and unauthorized-spend risks are hard gates.

## Master gates — current state

| Gate | State | Current evidence / next requirement |
|---|---|---|
| G0 CONTROL PLANE | GREEN | GitHub roadmap + handoff + decisions operational |
| G1 BOOKING HEALTHY | GREEN | booking incident resolved; no new regression |
| G2 MEASUREMENT READY | PARTIAL / PILOT-READY | Data Manager validate-only HTTP 200 + production promotion complete; first legitimate completed-visit import/dedupe/reconciliation still required before scale/Primary promotion |
| G3 GOOGLE BASELINES | PARTIAL | Ads/GBP/Search Console captured; GA4 live receipt/settings still open |
| G4 FOUNDATION CORRECTED | PARTIAL | production urgent-care landing/redirect CI fixed; GBP/GA4 cleanup remains |
| G5 ECONOMICS/PRIORITIES | PROVISIONAL | pilot can use documented provisional assumptions; authoritative economics still desired |
| G6 LOCAL LANDING PATH | GREEN | urgent-care production landing + redirects covered by green `main/4` smoke |
| G7 LOCAL PAID EXPERIMENT | PENDING FINAL READ-BACK | user changed geo option to Presence in Google Ads UI; fresh system read-back + final ad/policy status required before enable |
| G8 TRAVELER CAMPAIGN BUILD | IN PROGRESS / PAUSED | campaign/ad groups/keywords created PAUSED; dedicated policy-safe traveler landing is being built before RSAs/assets |
| G9 LOCAL GROWTH CYCLE | IN PROGRESS | GBP baseline exists; cleanup/reputation cadence remains |
| G10 AI PAID READY | WAITING_EXTERNAL | ChatGPT Ads account/eligibility not yet established |
| G11–G13 | PLANNED | partnership/content/intelligence/repeatable-cycle work follows priority lanes |

## Phase A — Measurement completion

A1 `DONE`: Google Data Manager auth/destination acceptance validated with a real `validateOnly=true` request returning HTTP 200. No real click ID was fabricated.

A2 `DONE`: compatible measurement + growth batch promoted to production through PR #104.

A3 `DONE for production deployment`: recovery PR #105 aligned Jenkins smoke expectations with intentional urgent-care redirects. Production `main` `5e34eea5ca5c1b78a0aeceb2a4fa287b7b15e1ae`; Jenkins `main/4` SUCCESS.

A4 `IN-PILOT ACCEPTANCE`: on first legitimate completed appointment with GCLID/WBRAID/GBRAID, send one controlled `visit_completed`, replay the same transaction ID to verify idempotency/dedupe, reconcile to Google Ads, then decide whether `Visit Completed` can graduate from Secondary. This is a scale gate, not a blocker to a small controlled pilot once launch configuration is verified.

## Phase B — Google Ads growth system

B1/B2 legacy evidence: preserve historical Smart campaign evidence; keep legacy Smart campaign paused. Do not relaunch it as primary acquisition. Leave Google-managed Local Services campaign unchanged until its role is understood.

### B3 — Local urgent-care Search pilot

Campaign `24414014329` exists PAUSED with Manual CPC, provisional $40/day budget, five-mile Beverly Hills proximity, clinic-hours schedule, Exact/Phrase positives, campaign negatives, call/callout/sitelink assets and three paused ad groups/RSAs.

The user changed the positive geo option in Google Ads UI to Presence-only on 2026-10-29. Connected Windsor data remains cached on the old `PRESENCE_OR_INTEREST` value and cannot be force-refreshed on the current plan. Treat the UI save as latest direct evidence, but require a fresh system read-back before enable.

DECISION — keep this local urgent-care campaign Presence-only. Do not use it to capture people outside the area merely because they show destination interest. Immediate local intent and pre-arrival traveler intent are separate acquisition problems.

After fresh geo/policy read-back: controlled launch only within existing finite guardrails → early search-term review/negatives → completed-visit acceptance when the first legitimate event occurs. Do not scale from CTR/clicks alone.

### B4/B5 — Demand and economics

Initial demand research supports core Beverly Hills/near-me urgent-care intent ahead of low-volume variants. Economics remain provisional; replace assumptions with authoritative clinic economics when available without blocking safe setup work.

### B6 — HIGH PRIORITY: Traveler / pre-arrival Search campaign

FACT — campaign created PAUSED in Google Ads on 2026-10-29:
- campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`;
- Manual CPC;
- configured $20/day budget while PAUSED; this is not launch/spend authorization;
- United States geo target;
- English;
- schedule 06:00–22:00 daily in account time zone;
- declared as not containing EU political advertising.

PAUSED ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — $3.50 default CPC.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — $3.50 default CPC.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — $4.00 default CPC.

FACT — 36 Exact/Phrase positive keywords created PAUSED across the three ad groups. 32 campaign negatives added, including overlap/waste controls and temporary exclusions for prescription/refill/telemedicine/virtual intent while healthcare certification is pending.

DATA NOTE — connected Search Console filtering for recent hotel/traveler/tourist/visitor terms returned no rows. Treat this as an explicit paid hypothesis; do not claim proven organic volume.

Strategy:
- objective: qualified appointments from travelers, tourists, hotel guests and visitors explicitly planning care in Beverly Hills;
- source-market approach: initial United States targeting, with explicit Beverly Hills + traveler/visitor/hotel query language carrying destination intent;
- match control: Exact/Phrase only initially;
- overlap control: `near me` is excluded from this campaign so immediate local intent can flow to the local urgent-care campaign;
- policy split: this campaign initially advertises in-person clinic and approved hotel/mobile care only; telemedicine/prescription claims remain gated by LegitScript + Google healthcare certification;
- measurement: dedicated campaign/source naming, click-ID capture, first-party attribution and completed-visit feedback;
- budget: campaign remains PAUSED until separate launch/budget authorization and all launch gates pass.

B6-LANDING `ACTIVE`: do not use the existing `/hotel-traveler-care` page as the paid destination because it contains virtual-care/prescription-refill language. Build and production-validate a dedicated policy-safe landing:
`https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

Landing requirements: Beverly Hills traveler intent, clinic + approved hotel/mobile options only, booking/call CTA, actual hours/address/phone, same-day only `when available`, 911/not-emergency-care, no prescription/refill/telemedicine advertising claims, first-party attribution, no intentional GA4 injection on health-intent surface.

After production landing is green: create PAUSED RSAs + policy-safe call/callout/sitelink assets, then perform final geo/policy read-back. Do not enable or spend yet.

### B7 — Google healthcare certification / policy remediation

FACT — `Clinic Services` sitelink pointing to `/services` is disapproved for `PRESCRIPTION_DRUG_SALE` with missing certification for the United States and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete or hide the legitimate telemedicine/prescription-refill service merely to bypass policy. Resolve the root requirement through certification.

Required sequence:
1. Dr. Farah decides/proceeds with LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`.
2. After LegitScript approval, submit Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services.
3. Re-read the affected sitelink and relevant ad/asset policy statuses.
4. Keep health-personalization restrictions intact; certification is not permission to use prohibited health remarketing/Customer Match workarounds.

Current standard LegitScript pricing verified 2026-10-29: $975 non-refundable application fee + $2,150 annual certification after approval; standard first-year total $3,125.

WAITING_EXTERNAL — Issue #106 tracks Dr. Farah's decision/application/approval. Do not request/store portal passwords, payment data, PHI or patient records.

B7 site-readiness: replace draft `frontend/terms.html` and placeholder `frontend/notice-of-privacy-practices.html` with clinic/legal-approved content before final certification readiness. Engineering can prepare implementation/drafts; clinic/legal must provide/approve actual legal facts.

## Phase C — SEO / landing growth

C1 prioritize high-intent local urgent-care terms around positions 4–20. Traveler/pre-arrival is a separate paid/organic hypothesis under B6, not mixed into the local urgent-care pilot.

C2 urgent-care production path is deployed and green. Continue Search Console indexing/canonical monitoring. `/book` and `/patient-registration` remain noindex and excluded from sitemap.

C3 next landing priority is the dedicated traveler/pre-arrival page required by B6. Add to sitemap and production validation before using as an ad destination.

## Phase D — GBP / Maps / reputation

D1 inspect Google updates/special hours/factual accuracy. D2 selectively clean duplicate/aggressive service entries. D3 establish neutral privacy-safe review request/response cadence. D4 maintain factual local competitor loop.

## Phase E — GA4 / cross-channel measurement

Soft validation remains: safe Realtime/DebugView event on allowlisted low-risk page; timezone/currency; Enhanced Measurement; consent; allowlist/excluded sensitive-page verification. GA4 is diagnostic; first-party DB is source/click→appointment truth; Google Ads offline conversion is optimization feedback.

## Phase F — Controlled Google Search experiments

Local campaign may launch only after fresh Presence-only read-back and acceptable final core ad/policy state. First real completed visit becomes the in-pilot G2 acceptance.

Traveler campaign remains PAUSED until its dedicated landing is production-green, its RSAs/assets are reviewed, geo/policy state is acceptable and separate spend authorization exists.

Both campaigns use early search-term waste control and completed-visit economics as the decision standard.

## Phase G — Stable offline conversion operations

After first real controlled import succeeds, automate eligible `visit_completed` rows with idempotency/import state, safe batching, bounded retries, quarantine for permanent failures, non-sensitive health metrics and periodic Google Ads reconciliation. This is operational automation, not autonomous spend.

## Phase H — ChatGPT Ads

Start eligibility/account-onboarding investigation once final Google launch configuration is stable; it may proceed while Google pilots accumulate performance data and while LegitScript is externally pending where that certification is not a ChatGPT Ads prerequisite. Current facts: ChatGPT Ads Manager installed; prior account discovery found no accessible clinic ad account; Windsor exposes `openai_ads` but no account is connected.

No ChatGPT spend until healthcare eligibility, account access, measurement and finite budget authorization are satisfied.

## Deferred / durable blockers

- B-002 SCALE GATE: first legitimate paid completed-visit import + replay/dedupe + Google reconciliation.
- B-004 READ-BACK GATE: local Google Ads UI changed to Presence-only; fresh live system read-back still required before enable because connected data is cached.
- B-005 SOFT: GA4 live receipt/settings verification.
- B-006 SOFT: authoritative clinic economics/capacity inputs.
- B-007 WAITING_EXTERNAL: ChatGPT Ads eligibility/account access.
- B-008 WAITING_EXTERNAL / HIGH PRIORITY: LegitScript + Google healthcare certification. External response must not stop independent safe lanes.
- B-009 ACTIVE: traveler/pre-arrival landing must pass CI and production promotion before traveler RSAs use it.

## Immediate execution queue

1. Require Jenkins `dev/29` green on PR #108 merge SHA; diagnose if it fails.
2. Complete `growth/traveler-prearrival-landing-20261029`: dedicated traveler landing + sitemap + handoff/roadmap state; PR to `dev`; require exact-head CI green; merge.
3. Promote validated traveler landing to `main` under normal production gates; require production CI/smoke evidence.
4. Create traveler RSAs and safe assets PAUSED against the production traveler landing; do not enable/spend.
5. Obtain fresh local-campaign Presence-only read-back; final policy/readiness review before local pilot enable.
6. Dr. Farah continues LegitScript external lane; after approval, complete Google healthcare certification and re-read affected asset.
7. First legitimate completed visit with eligible click ID → Data Manager live import + replay/dedupe + reconciliation.
8. Continue GBP cleanup + Search Console monitoring + GA4 soft validation + certification-site readiness.
9. Start ChatGPT Ads eligibility/account-onboarding after final Google launch configuration is stable.
10. Scale/modify/stop only from completed-visit economics and measurement confidence.
