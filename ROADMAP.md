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
| G7 FIRST PAID EXPERIMENT | PENDING FINAL READ-BACK | user changed geo option to Presence in Google Ads UI; fresh system read-back + final ad/policy status required before enable |
| G8 LOCAL GROWTH CYCLE | IN PROGRESS | GBP baseline exists; cleanup/reputation cadence remains |
| G9 AI PAID READY | WAITING_EXTERNAL | ChatGPT Ads account/eligibility not yet established |
| G10–G13 | PLANNED | partnership/content/intelligence/repeatable-cycle work follows priority lanes |

## Phase A — Measurement completion

A1 `DONE`: Google Data Manager auth/destination acceptance validated with a real `validateOnly=true` request returning HTTP 200. No real click ID was fabricated.

A2 `DONE`: compatible measurement + growth batch promoted to production through PR #104.

A3 `DONE for production deployment`: production recovery PR #105 aligned Jenkins smoke expectations with intentional urgent-care redirects. Current `main` `5e34eea5ca5c1b78a0aeceb2a4fa287b7b15e1ae`; Jenkins `main/4` SUCCESS.

A4 `IN-PILOT ACCEPTANCE`: on first legitimate completed appointment with GCLID/WBRAID/GBRAID, send one controlled `visit_completed`, replay the same transaction ID to verify idempotency/dedupe, reconcile to Google Ads, then decide whether `Visit Completed` can graduate from Secondary. This is a scale gate, not a blocker to a small controlled pilot once final launch configuration is verified.

## Phase B — Google Ads growth system

B1/B2 legacy evidence: preserve historical Smart campaign evidence; keep legacy Smart campaign paused. Do not relaunch it as primary acquisition. Leave Google-managed Local Services campaign unchanged until its role is understood.

### B3 — Local urgent-care Search pilot

B3 architecture `MOSTLY DONE`: Search pilot `24414014329` exists PAUSED with Manual CPC, provisional $40/day budget, five-mile Beverly Hills proximity, clinic-hours schedule, Exact/Phrase positives, campaign negatives, call/callout/sitelink assets and three paused ad groups.

B3 ads `DONE / PAUSED`: three paused RSAs now exist against `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`:
- `196894367450~829832740743` — Beverly Hills intent;
- `204328258769~829881874987` — Near Me intent;
- `199388744537~829963008380` — Walk-In/Same-Day intent.
They are intentionally paused and cannot spend.

B4 demand research `DONE for initial pilot`: account/Keyword Planner + Search Console evidence supports core Beverly Hills/near-me urgent-care intent ahead of low-volume private/pre-op variants.

B5 pilot economics `PROVISIONAL`: retain finite learning budget and conservative Manual CPC until real completed-visit evidence exists. Replace assumptions with authoritative clinic economics when available; do not block launch configuration on this soft gap.

B-004 `UI CHANGED / READ-BACK PENDING`: user changed the positive geo option in Google Ads UI from `PRESENCE_OR_INTEREST` to Presence-only on 2026-10-29. Connected Windsor data is cached and still reports the prior value; the current Windsor plan does not permit forced refresh. Before any campaign/ad-group/ad enable action, obtain a fresh live system read-back confirming Presence-only. Do not mistake the stale cached value for proof the UI save failed.

DECISION — keep the first urgent-care campaign Presence-only. It is intended for people physically in/regularly in the service area who have immediate local medical intent. Pre-arrival traveler demand will not be forced into this campaign.

After fresh geo read-back: final read-back of campaign/ad/policy state → enable only within existing controlled pilot authorization/guardrails if no new hard blocker appears → early search-term review/negative additions → completed-visit acceptance when first legitimate event occurs.

### B6 — HIGH PRIORITY: Traveler / pre-arrival Search campaign

Create a second, separate Search campaign to capture people planning a Beverly Hills trip who may want medical access before they arrive. This is a distinct acquisition hypothesis, not an expansion of the local urgent-care campaign.

Working campaign name: `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot`.

Strategy:
- **Primary objective:** generate qualified appointments from travelers, tourists, hotel guests and visitors who explicitly plan to receive care in Beverly Hills.
- **Initial geography:** United States Presence-only at the source-market level. Do not initially depend on Beverly Hills `Presence or interest`, because that broad Google inference can mix weak destination interest with real medical intent. Let explicit query language prove the destination intent.
- **Keyword architecture:** Exact/Phrase first. Build around explicit combinations of Beverly Hills + doctor/medical care/urgent care + traveler/tourist/visitor/hotel intent. Example themes: doctor for tourists in Beverly Hills, traveler medical care Beverly Hills, doctor near Beverly Hills hotel, urgent care for visitors Beverly Hills, hotel physician Beverly Hills where the service is factually available.
- **Landing architecture:** dedicated hotel/traveler care page, with clear location/service-area/hours, in-person/mobile availability only where factual, booking + call CTAs, no guaranteed same-day claim, and 911/not-emergency-room language.
- **Policy split:** prepare and advertise in-person/pre-arrival traveler care independently. Any copy or landing claims involving telemedicine prescribing or prescription refills remain gated by LegitScript + Google healthcare certification.
- **Overlap control:** traveler-specific modifiers should route traveler intent to this campaign; use search-term analysis and campaign negatives to reduce cannibalization without excluding legitimate local travelers from care.
- **Measurement:** dedicated campaign/source naming, UTM convention, click-ID capture and completed-visit feedback. Judge by completed visits and economics, not clicks/CTR alone.
- **Budget/control:** build and validate the campaign PAUSED first. No new spend until an explicit budget is authorized under the existing spend-control rules.
- **Expansion rule:** after enough real completed-visit evidence, test selected source metros/states and, only as a controlled experiment, compare broader destination-interest targeting against the keyword-led baseline. Do not start broad.

Execution priority: HIGH. Build the demand/keyword map, negative/overlap plan, landing specification, ad-copy specification and measurement naming while LegitScript is pending. Create the campaign PAUSED once configuration is validated.

### B7 — Google healthcare certification / policy remediation

FACT — `Clinic Services` sitelink pointing to `/services` is disapproved for `PRESCRIPTION_DRUG_SALE` with missing certification for the United States and is limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete or hide the legitimate telemedicine/prescription-refill service merely to bypass policy. Resolve the root requirement through certification.

Required sequence:
1. Dr. Farah decides whether to proceed and completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`.
2. After LegitScript approval, submit Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services.
3. Re-read the affected sitelink and all relevant ad/asset policy statuses.
4. Keep health-personalization restrictions intact; certification is not permission to use prohibited health remarketing/Customer Match workarounds.

Current verified standard LegitScript pricing (2026-10-29): $975 non-refundable application fee per website + $2,150 annual certification fee per website after approval; standard first-year total $3,125. Optional expedited processing is separate.

WAITING_EXTERNAL — Issue #106 tracks this. Dr. Farah must complete/approve the external application and provide the resulting certification/approval reference. Do not request or store portal passwords, payment data, PHI or patient records.

B7 site-readiness subtask: replace draft `frontend/terms.html` and placeholder `frontend/notice-of-privacy-practices.html` with clinic/legal-approved content before certification completion/final review. Engineering can prepare structure and implementation; clinic/legal must provide/approve the actual legal facts.

## Phase C — SEO / landing growth

C1 opportunity map: prioritize high-intent local urgent-care terms around positions 4–20, especially Beverly Hills/near-me themes. Traveler/pre-arrival terms are now a high-priority separate paid/organic hypothesis under B6 rather than being mixed into the local urgent-care pilot.

C2 technical/indexing: production urgent-care landing, sitemap entry and legacy redirects are deployed; `main/4` smoke is green. Continue Search Console indexing/canonical monitoring. `/book` and `/patient-registration` remain noindex and excluded from sitemap.

C3 landing map: first urgent-care paid/organic landing path is ready. Next priority is the dedicated traveler/hotel landing refinement required by B6; other dedicated pages should still be justified by demand/economics rather than created by default.

## Phase D — GBP / Maps / reputation

D1 inspect `has_google_updated`, current special hours and factual accuracy. D2 selectively clean duplicate/aggressive service-catalogue entries; do not bulk-delete. D3 establish neutral privacy-safe review request/response cadence. D4 maintain local competitor loop using factual visibility/category/review/hours/booking evidence.

## Phase E — GA4 / cross-channel measurement

Soft validation remains: safe Realtime/DebugView event on an allowlisted low-risk page; timezone/currency; Enhanced Measurement; consent behavior; selected-page allowlist and excluded sensitive-page verification. GA4 is diagnostic; first-party DB is source/click→appointment truth; Google Ads offline conversion is optimization feedback; Search Console and GBP remain their own authorities.

## Phase F — Controlled Google Search experiment

Local pilot prerequisite: G1 green + G6 green + fresh Presence-only read-back + acceptable final core ad/policy state. Do not wait for a real completed visit before generating the first traffic; that event is the in-pilot G2 acceptance.

Pilot must retain exact local intent/geography, finite budget, controlled match types/negatives, relevant landing, `Visit Completed` linkage, booking/call diagnostics, stop/modify/scale thresholds and early search-term waste review. Do not scale from CTR/clicks alone.

Traveler campaign remains PAUSED during configuration. Its in-person/pre-arrival portion can be prepared while LegitScript is pending; telemedicine/prescription advertising claims remain certification-gated.

## Phase G — Stable offline conversion operations

After first real controlled import succeeds, automate eligible `visit_completed` rows with idempotency/import state, safe batching, bounded retries, quarantine for permanent failures, non-sensitive health metrics and periodic Google Ads reconciliation. This is operational automation, not autonomous spend.

## Phase H — ChatGPT Ads

Start eligibility/account-onboarding investigation once final Google launch configuration is complete; it may proceed while Google pilots accumulate real performance data and while LegitScript is externally pending, provided the ChatGPT Ads healthcare eligibility path itself is satisfied. Current facts: ChatGPT Ads Manager is installed but prior account discovery found no accessible clinic ad account; Windsor exposes `openai_ads` but no account is connected.

H1 verify current healthcare/urgent-care eligibility and obtain/confirm account access. H2 define incremental channel hypothesis versus Google Search. H3 use dedicated source attribution and completed-visit outcome where compliant. H4 only then create a finite-budget pilot with explicit stop/scale rules. No ChatGPT spend until eligibility, account access, measurement and budget authorization are all satisfied.

## Deferred / durable blockers

- B-002 SCALE GATE: first legitimate paid completed-visit import + replay/dedupe + Google reconciliation.
- B-004 READ-BACK GATE: Google Ads UI was changed to Presence-only; fresh live system read-back still required before enable because connected data is cached.
- B-005 SOFT: GA4 live receipt/settings verification.
- B-006 SOFT: authoritative clinic economics/capacity inputs.
- B-007 WAITING_EXTERNAL: ChatGPT Ads eligibility/account access.
- B-008 WAITING_EXTERNAL / HIGH PRIORITY: LegitScript + Google healthcare certification for telemedicine/prescription-drug services. External response must not stop independent safe lanes.
- Operational follow-up: keep `PROJECT_HANDOFF.md` synchronized after material state changes; do not let stale pre-release instructions become execution gates again.

## Immediate execution queue

1. Obtain fresh live read-back of campaign `24414014329` confirming Presence-only; keep campaign/ad groups/ads paused until then.
2. Dr. Farah: decide/proceed with LegitScript Healthcare Merchant Certification. Project: maintain Issue #106, prepare site/legal readiness, and after approval complete Google healthcare certification. Do not delete the affected service to bypass certification.
3. HIGH PRIORITY parallel lane: build the second `Traveler Care | Beverly Hills | Pre-Arrival` campaign specification and PAUSED configuration, including keyword map, overlap negatives, landing requirements, ad copy and measurement naming.
4. Final local Google Ads policy/ad status read-back; if acceptable and no hard gate remains, controlled launch under existing finite pilot guardrails.
5. First-hour/early search-term waste control and negatives as data arrives.
6. First legitimate completed visit with eligible click ID → Data Manager live import + replay/dedupe + reconciliation.
7. Parallel GBP cleanup + Search Console monitoring + GA4 soft validation + certification-site readiness.
8. ChatGPT Ads eligibility/account-onboarding work after final Google launch configuration is complete, without waiting for long-term Google optimization learning or external certification where not required by that channel.
9. Scale/modify/stop only from completed-visit economics and measurement confidence.