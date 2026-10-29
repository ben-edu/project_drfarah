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
| G2 MEASUREMENT READY | PARTIAL / PILOT-READY | Data Manager `validateOnly` HTTP 200 + production promotion complete; first legitimate completed-visit import/dedupe/reconciliation still required before scale/Primary promotion |
| G3 GOOGLE BASELINES | PARTIAL | Ads/GBP/Search Console captured; GA4 live receipt/settings still open |
| G4 FOUNDATION CORRECTED | PARTIAL | production landing/redirect CI fixed; GBP/GA4 cleanup remains |
| G5 ECONOMICS/PRIORITIES | PROVISIONAL | pilot can use documented provisional assumptions; authoritative economics still desired |
| G6 LANDING PATHS | GREEN for first Search pilot | production landing + redirects directly covered by green `main/4` smoke |
| G7 FIRST PAID EXPERIMENT | BLOCKED | B-004 Presence-only geo setting must be fixed/read back before enable |
| G8 LOCAL GROWTH CYCLE | IN PROGRESS | GBP baseline exists; cleanup/reputation cadence remains |
| G9 AI PAID READY | WAITING_EXTERNAL | ChatGPT Ads account/eligibility not yet established |
| G10–G13 | PLANNED | partnership/content/intelligence/repeatable-cycle work follows priority lanes |

## Phase A — Measurement completion

A1 `DONE`: Google Data Manager auth/destination acceptance validated with a real `validateOnly=true` request returning HTTP 200. No real click ID was fabricated.

A2 `DONE`: compatible measurement + growth batch promoted to production through PR #104.

A3 `DONE for production deployment`: production recovery PR #105 aligned Jenkins smoke expectations with intentional urgent-care redirects. Current `main` `5e34eea5ca5c1b78a0aeceb2a4fa287b7b15e1ae`; Jenkins `main/4` SUCCESS.

A4 `IN-PILOT ACCEPTANCE`: on first legitimate completed appointment with GCLID/WBRAID/GBRAID, send one controlled `visit_completed`, replay the same transaction ID to verify idempotency/dedupe, reconcile to Google Ads, then decide whether `Visit Completed` can graduate from Secondary. This is a scale gate, not a blocker to a small controlled pilot once B-004 is fixed.

## Phase B — Google Ads pilot

B1/B2 legacy evidence: preserve historical Smart campaign evidence; keep legacy Smart campaign paused. Do not relaunch it as primary acquisition. Leave Google-managed Local Services campaign unchanged until its role is understood.

B3 architecture `MOSTLY DONE`: Search pilot `24414014329` exists PAUSED with Manual CPC, provisional $40/day budget, five-mile Beverly Hills proximity, clinic-hours schedule, Exact/Phrase positives, campaign negatives, call/callout/sitelink assets and three paused ad groups.

B3 ads `DONE / PAUSED`: three paused RSAs now exist against `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`:
- `196894367450~829832740743` — Beverly Hills intent;
- `204328258769~829881874987` — Near Me intent;
- `199388744537~829963008380` — Walk-In/Same-Day intent.
They are intentionally paused and cannot spend.

B4 demand research `DONE for initial pilot`: account/Keyword Planner + Search Console evidence supports core Beverly Hills/near-me urgent-care intent ahead of low-volume private/pre-op variants.

B5 pilot economics `PROVISIONAL`: retain finite learning budget and conservative Manual CPC until real completed-visit evidence exists. Replace assumptions with authoritative clinic economics when available; do not block launch configuration on this soft gap.

B-004 `HARD LAUNCH BLOCKER`: last verified positive geo option is `PRESENCE_OR_INTEREST`. Before any campaign/ad-group/ad enable action, change to Presence-only — people in or regularly in the targeted locations — and read it back. Windsor can edit proximity criteria but does not expose this positive-geo-type setting. Do not mistake re-setting the five-mile radius for fixing B-004.

After B-004: final read-back of campaign/ad/policy state → enable only within existing controlled pilot authorization/guardrails → early search-term review/negative additions → completed-visit acceptance when first legitimate event occurs.

## Phase C — SEO / landing growth

C1 opportunity map: prioritize high-intent local urgent-care terms around positions 4–20, especially Beverly Hills/near-me themes; keep pre-op/traveler/VIP as separate hypotheses.

C2 technical/indexing: production urgent-care landing, sitemap entry and legacy redirects are deployed; `main/4` smoke is green. Continue Search Console indexing/canonical monitoring. `/book` and `/patient-registration` remain noindex and excluded from sitemap.

C3 landing map: first urgent-care paid/organic landing path is ready. Next dedicated landing pages should be justified by demand/economics rather than created by default.

## Phase D — GBP / Maps / reputation

D1 inspect `has_google_updated`, current special hours and factual accuracy. D2 selectively clean duplicate/aggressive service-catalogue entries; do not bulk-delete. D3 establish neutral privacy-safe review request/response cadence. D4 maintain local competitor loop using factual visibility/category/review/hours/booking evidence.

## Phase E — GA4 / cross-channel measurement

Soft validation remains: safe Realtime/DebugView event on an allowlisted low-risk page; timezone/currency; Enhanced Measurement; consent behavior; selected-page allowlist and excluded sensitive-page verification. GA4 is diagnostic; first-party DB is source/click→appointment truth; Google Ads offline conversion is optimization feedback; Search Console and GBP remain their own authorities.

## Phase F — Controlled Google Search experiment

Launch prerequisite: G1 green + G6 green + B-004 fixed/read back. Do not wait for a real completed visit before generating the first traffic; that event is the in-pilot G2 acceptance.

Pilot must retain exact local intent/geography, finite budget, controlled match types/negatives, relevant landing, `Visit Completed` linkage, booking/call diagnostics, stop/modify/scale thresholds and early search-term waste review. Do not scale from CTR/clicks alone.

## Phase G — Stable offline conversion operations

After first real controlled import succeeds, automate eligible `visit_completed` rows with idempotency/import state, safe batching, bounded retries, quarantine for permanent failures, non-sensitive health metrics and periodic Google Ads reconciliation. This is operational automation, not autonomous spend.

## Phase H — ChatGPT Ads

Start eligibility/account-onboarding investigation once B-004 and final Google launch configuration are complete; it may proceed while the Google pilot accumulates real performance data. Current facts: ChatGPT Ads Manager is installed but prior account discovery found no accessible clinic ad account; Windsor exposes `openai_ads` but no account is connected.

H1 verify current healthcare/urgent-care eligibility and obtain/confirm account access. H2 define incremental channel hypothesis versus Google Search. H3 use dedicated source attribution and completed-visit outcome where compliant. H4 only then create a finite-budget pilot with explicit stop/scale rules. No ChatGPT spend until eligibility, account access, measurement and budget authorization are all satisfied.

## Deferred / durable blockers

- B-002 SCALE GATE: first legitimate paid completed-visit import + replay/dedupe + Google reconciliation.
- B-004 HARD LAUNCH GATE: Google Ads positive geo target type must be Presence-only.
- B-005 SOFT: GA4 live receipt/settings verification.
- B-006 SOFT: authoritative clinic economics/capacity inputs.
- B-007 WAITING_EXTERNAL: ChatGPT Ads eligibility/account access.
- Operational follow-up: keep `PROJECT_HANDOFF.md` synchronized after material state changes; do not let stale pre-release instructions become execution gates again.

## Immediate execution queue

1. Fix/read back B-004 Presence-only setting while keeping all pilot objects paused.
2. Final Google Ads policy/status read-back; if clean, controlled launch under existing finite pilot guardrails.
3. First-hour/early search-term waste control and negatives as data arrives.
4. First legitimate completed visit with eligible click ID → Data Manager live import + replay/dedupe + reconciliation.
5. Parallel GBP cleanup + Search Console monitoring + GA4 soft validation.
6. ChatGPT Ads eligibility/account-onboarding work after Google launch configuration is complete, without waiting for long-term Google optimization learning.
7. Scale/modify/stop only from completed-visit economics and measurement confidence.