# Dr. Farah VIP Urgent Care — Master Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Canonical roadmap:** this file only  
> **Integration branch:** `dev`  
> **Production branch:** `main`  
> **Exact resume point:** `PROJECT_HANDOFF.md`  
> **GitHub:** durable project memory, code, decisions, roadmap and handoff  
> **OpenProject:** authoritative for live work-package metadata  
> **Live systems:** authoritative for their own current state

**Operating mode:** Growth Acceleration / parallel execution.  
**Roadmap refreshed:** 2026-10-31.

---

## 1. Mission

Build and operate one integrated growth system across Google Ads, Search Console, Google Business Profile, GA4, first-party attribution, completed-visit feedback, conversion-focused website/landing paths, service economics, traveler/hotel growth, pre-op referrals, physician-led content, ChatGPT Ads and Growth Intelligence.

Primary business outcome: completed visits and defensible economics, not clicks, impressions or superficial conversions alone.

---

## 2. Authority and execution rules

Authority order when sources disagree:
1. verified clinic/business fact from Dr. Farah or authoritative clinic record;
2. live production/account system for its own current state;
3. approved `docs/DECISIONS.md`;
4. `PROJECT_HANDOFF.md` + this roadmap;
5. stable repository specs/runbooks/code;
6. OpenProject execution metadata;
7. historical reports/chats.

Execution rules:
- parallel by default; an external blocker in one lane does not stop safe independent work elsewhere;
- production is the destination for validated work;
- batch related work before CI and avoid redundant Jenkins jobs;
- normal Git flow is `feature/fix/docs -> dev -> main`; current `main` must be contained in `dev` before promotion;
- completed visit is the primary business outcome;
- never send unnecessary PII/PHI, reason-for-visit or clinical context to marketing platforms;
- real-data tests that inherently require traffic belong inside controlled pilots;
- no silent defects: fix or durably track discovered problems.

---

## 3. Master gates — current state

| Gate | State | Current evidence / next requirement |
|---|---|---|
| G0 CONTROL PLANE | GREEN | GitHub roadmap/handoff/decisions + Git release strategy operational |
| G1 BOOKING HEALTHY | GREEN | booking incident resolved; no known regression |
| G2 MEASUREMENT READY | PARTIAL / PILOT-READY | Google Data Manager validate-only HTTP 200; first legitimate live completed-visit import/replay/reconciliation remains scale gate |
| G3 GOOGLE BASELINES | PARTIAL | Ads/GBP/Search Console captured; GA4 receipt/settings soft validation remains |
| G4 WEBSITE / LANDING FOUNDATION | PARTIAL / ACTIVE | paid landing paths healthy; real service imagery corrected; site still needs additional responsive/navigation and visual development |
| G5 ECONOMICS / PRIORITIES | PROVISIONAL | pilot economics documented; authoritative clinic economics still desired |
| G6 LANDING PATHS | GREEN for current paid pilots | urgent-care + traveler paid landings production-ready |
| G7 LOCAL PAID EXPERIMENT | READY EXCEPT POLICY / LAUNCH AUTHORIZATION | local campaign PAUSED; geo `PRESENCE`; policy/readiness + explicit spend authorization before enable |
| G8 TRAVELER PAID EXPERIMENT | BUILT / PAUSED | 3 ad groups, 36 positives, 32 negatives, assets and 3 RSAs; geo `PRESENCE`; policy/readiness + explicit spend authorization remain |
| G9 LOCAL GROWTH CYCLE | IN PROGRESS | GBP baseline exists; cleanup/reputation cycle remains |
| G10 AI PAID READY | WAITING_EXTERNAL | ChatGPT Ads account/eligibility not established |
| G11 PARTNERSHIP EXPERIMENTS | PLANNED / PARTIAL PREP | traveler/hotel + pre-op referral engines remain active roadmap lanes |
| G12 CONTENT ENGINE | PLANNED | query/partner/economics-led physician content |
| G13 GROWTH INTELLIGENCE | PLANNED / PARTIAL FOUNDATION | source→appointment exists; completed-visit/cost/economics loop still maturing |

---

# Phase A — Measurement completion

### A1 — Google Data Manager technical acceptance
DONE. Real `validateOnly=true` request returned HTTP 200 after API/auth/runtime remediation.

### A2 — Production measurement promotion
DONE. Data Manager / attribution runtime was promoted through validated production releases.

### A3 — First legitimate completed-visit acceptance
IN PILOT / SCALE GATE. On the first legitimate completed appointment carrying GCLID/WBRAID/GBRAID:
1. validate eligible row;
2. record one controlled `visit_completed`;
3. replay deterministic transaction ID to validate dedupe/idempotency;
4. reconcile Google Ads with internal completed appointment;
5. keep `Visit Completed` Secondary until trusted.

Do not fabricate a click ID or conversion.

---

# Phase B — Google Ads growth system

## B1 — Legacy campaigns
- Smart campaign `22552983079` remains PAUSED; preserve forensic value and do not relaunch as primary acquisition.
- Google-managed Local Services campaign `23637947414` must not be changed without a specific decision; live account state wins.

## B2 — Local urgent-care Search pilot
Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28`.

Current state:
- PAUSED; no authorized spend;
- Manual CPC; provisional configured budget $40/day;
- five-mile Beverly Hills targeting and clinic-hours schedule;
- Exact/Phrase positives + negatives; no Broad;
- three PAUSED ad groups and three PAUSED RSAs;
- landing: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`;
- live campaign readback confirms positive geo `PRESENCE`.

Ad groups:
1. `Urgent Care | Beverly Hills` — `196894367450` — $4.50 default CPC.
2. `Urgent Care | Near Me` — `204328258769` — $4.50 default CPC.
3. `Walk-In | Same-Day` — `199388744537` — $4.00 default CPC.

RSAs: `829832740743`, `829881874987`, `829963008380`.

Keyword Planner: `urgent care beverly hills` ~1,000 average monthly searches, MEDIUM competition, historical average CPC ~$3.56. Current Manual CPC range is directionally reasonable; do not change bids from planner data alone.

Next: fresh ad/asset policy readback when available, final readiness review, then controlled launch only with explicit spend authorization.

## B3 — Traveler / pre-arrival Search pilot
Campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`.

Current state:
- PAUSED; no authorized spend;
- Manual CPC; configured $20/day while paused;
- US geography, English, 06:00–22:00 schedule;
- EU political-ad declaration: No;
- live campaign readback confirms `PRESENCE`;
- 36 Exact/Phrase positives and 32 campaign negatives;
- dedicated landing: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

Ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — $3.50 default CPC.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — $3.50 default CPC.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — $4.00 default CPC.

RSAs: `829861283229`, `829861321812`, `829991120837`.

Policy-safe assets already created: four callouts, one structured snippet, four sitelinks. Call asset remains unresolved under issue #110.

Keyword evidence: ultra-specific traveler+Beverly Hills seeds had no reportable volume; `hotel doctor` / `doctor at hotel` ~140 US searches each and historical CPC ~$2.44; `doctor beverly hills` ~260 but ~$27 historical CPC; `concierge doctor beverly hills` ~590 and ~$10.72. DECISION: start precise and do not broaden blindly.

## B4 — Healthcare certification / policy remediation
FACT — sitelink `Clinic Services` asset `434419668405` to `/services` is disapproved for `PRESCRIPTION_DRUG_SALE` with missing US certification and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not hide/delete a legitimate telemedicine/prescription-refill service to bypass policy.

Path:
1. Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`.
2. After approval, complete Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services.
3. Re-read affected asset and all ads/assets across both Search campaigns.
4. Preserve separate health-sensitive personalization restrictions.

Issue #106 tracks this lane. Dr. Farah has now responded to the project; the response must be reviewed in the next Google Ads step. Do not infer certification approval until the response/evidence is inspected.

Current standard LegitScript pricing last verified 2026-10-29: $975 application fee + $2,150 annual certification after approval = $3,125 standard first-year total.

Site readiness still includes clinic/legal-approved Terms and Notice of Privacy Practices before final certification readiness.

## B5 — Call asset / mandatory post-certification review
Issue #110 tracks:
- healthcare/HIPAA-safe resolution of Call Ads Supplemental Terms / Communication Features;
- Google Support exclusion from monitoring/recording if required by clinic/legal determination;
- retry call asset only after the compliance path is resolved;
- mandatory post-certification review of both campaigns, all ads/assets, policies and landing destinations.

Do not blindly accept call-recording terms. Call recording remains off unless clinic/legal explicitly approves.

Current connector limitation: campaign-level reads work, while ad/asset policy reads may return zero rows even with inactive objects included; zero rows are a DATA_GAP, not approval.

---

# Phase C — Search Console / SEO / landing growth

Search Console property: `sc-domain:drfarahvipurgentcare.com`.

High-priority evidence:
- `urgent care near me`: 120 impressions / avg position 9.73 / 0 clicks;
- `urgent care beverly hills`: 40 / 11.1 / 0 clicks;
- `beverly hills urgent care`: 25 / 11.68 / 0 clicks;
- `medical clearance for surgery near me`: 30 / 3.43 / 0 clicks;
- `medical clearance near me`: 9 / 1.56 / 0 clicks;
- `vip urgent care`: 95 impressions / avg position 1.16 / CTR 2.11%.

The first urgent-care + Pre-Op SEO title/meta/on-page improvement batch is production-deployed. Continue monitoring 28-day movement and use real query evidence for later content/landing work.

Production indexing model is intentional: staging/source may contain `noindex`; `scripts/prepare-production-frontend.sh` removes it for production and installs production robots/sitemap behavior. `/book` and `/patient-registration` remain noindex unless strategy changes explicitly.

IV, PRP/regenerative and weight-management organic search remain longer-term lanes; do not prioritize them above higher-intent urgent-care/Pre-Op opportunities without new evidence.

---

# Phase D — Website design, imagery, mobile UX and performance

Issue #114 remains the durable website/image-quality work item.

### Completed in the 2026-10-31 visual refresh
- user-supplied/approved service imagery was imported and mapped to service pages;
- PRP and Weight Loss no longer share the same service image;
- Urgent Care, IV, Pre-Op, Virtual, Hotel/Traveler and Traveler Medical use distinct service assets;
- legacy/fake test imagery is no longer part of active service-image mapping and should be removed from the release tree;
- service-image cache version advanced to avoid stale visual mapping;
- landing hero behavior was improved for mobile/tablet so imagery sits above content rather than behind text on narrower widths;
- staging visual review by the user confirmed the new images are materially better.

### Still open — site development is NOT complete
- mobile/tablet navigation remains a known UX defect: the menu/navigation bar is not adequately visible/usable on small screens;
- perform a dedicated responsive navigation implementation and QA pass across common mobile/tablet widths;
- continue visual hierarchy, spacing, typography, card consistency and section polish where needed;
- verify no service page reuses an inappropriate image and that crop/focal point remains acceptable across desktop/tablet/mobile;
- continue image performance work (`srcset`/`sizes`, intrinsic dimensions, LCP prioritization, below-fold lazy loading) without degrading sharpness;
- conduct accessibility and interaction QA after navigation changes;
- maintain a high-end, restrained clinical/VIP visual system rather than generic template styling.

This website-development lane is important but does not block the next Google Ads policy/certification work unless a defect materially affects paid landing usability, factual accuracy or conversion safety.

---

# Phase E — Google Business Profile / Maps / reputation

GBP location `locations/6719840585856592244`; primary category `Urgent care center`; captured baseline 5.0 / 109 reviews.

Next:
- validate regular/special hours, map/address, phone, website/booking links and categories;
- inspect Google-updated/pending profile changes;
- evaluate service catalogue selectively for factual alignment;
- establish privacy-safe neutral review request/response cadence;
- maintain factual local competitor visibility/review/hours/messaging loop.

---

# Phase F — GA4 / cross-channel measurement quality

GA4 property `489069776`; stream `11211773871`; Measurement ID `G-D58FTMF05S`.

Soft validation remains for approved low-risk surfaces: Realtime/DebugView receipt, timezone/currency, Enhanced Measurement, consent behavior and allowlist/exclusion verification.

Roles remain distinct:
- GA4 = behavioral diagnostics on approved surfaces;
- first-party DB = source/click→appointment linkage;
- Google Ads offline conversion = optimization feedback;
- Search Console = organic search truth;
- GBP = Maps/profile truth.

---

# Phase G — Controlled paid experiment / optimization cycle

Each pilot requires a named hypothesis, exact intent/geography, finite learning budget/hard spend ceiling, controlled keywords/negatives, relevant production landing, completed-visit linkage, stop/modify/scale thresholds and a review date.

Do not enable either current Search campaign until explicit launch/spend authorization is present and final policy/readiness review is acceptable. Search-term waste control begins early. Scale only on completed visits, defensible CAC/contribution, capacity and measurement confidence.

---

# Phase H — Stable offline conversion operations

After first controlled real conversion succeeds:
- identify eligible new completed-visit rows with click IDs;
- record import state/idempotency;
- batch safely;
- bounded retry transient failures;
- quarantine permanent/schema/auth failures;
- never print click IDs or patient data in routine logs;
- expose non-sensitive operational metrics;
- periodically reconcile to Google Ads.

---

# Phase I — AI / ChatGPT Ads paid channel

Treat as a future paid-acquisition lane. Verify current healthcare eligibility/policy/account access, define incremental hypothesis versus Google Search, use dedicated attribution and completed-visit outcome where permitted, and create only finite-budget pilots with explicit stop/scale rules.

Current facts: Ads Manager installed; prior discovery found no accessible clinic ad account; Windsor `openai_ads` has no connected account.

---

# Phase J — Service economics and capacity

For each priority service collect/estimate: completed visits, collected revenue, variable cost, physician/staff time, capacity, repeat/referral leverage, no-show burden, acquisition cost and policy/operational constraints. Rank by demand × contribution × capacity × differentiation × acquisition efficiency × strategic value.

---

# Phase K — Traveler / hotel / VIP partnership growth

Sequence: traveler baseline → existing hotel/concierge sources → target list → accurate service scope/response model → partner interviews → partner kit → attribution → small pilot → completed-visit/revenue/repeat-referral review.

No unsupported 24/7, mobile or response-time promise. Paid traveler Search is a separate acquisition experiment and does not replace the partnership lane.

---

# Phase L — Pre-Op referral engine

Sequence: baseline → economics/capacity → value proposition → warm referrer map → target surgeons/surgery centers → referral package/workflow → compliance review → small outreach pilot → completed clearance/repeat-referral/revenue review.

No per-patient/referral compensation without appropriate compliance review. Search Console medical-clearance visibility should inform the patient page while the B2B engine is developed separately.

---

# Phase M — Physician-led content / creative

Content priorities are fed by Search Console, Ads search terms, GBP/reviews, traveler/pre-op questions, website friction and service economics. Build reusable long-form, short-form, website and paid derivatives. Measure qualified business contribution, not views alone.

---

# Phase N — Growth Intelligence / recurring operating cycle

Sequence:
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

Growth Intelligence is not an EHR and must not become one.

---

## 4. Preserved OpenProject work-package identifiers

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

BG-10 exact child identifiers must be verified from OpenProject when needed.

---

## 5. Durable blockers / tracked issues

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — SCALE GATE only: first legitimate live completed-visit import + replay/dedupe + reconciliation.
- B-003 Local paid destination — CLOSED.
- B-004 Local campaign geo — CLOSED; live readback `PRESENCE`.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 authoritative clinic economics/capacity — SOFT.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL.
- B-008 LegitScript + Google healthcare certification — ACTIVE EXTERNAL / HIGH PRIORITY; issue #106; Dr. Farah has responded and response review is next.
- B-009 Traveler landing production readiness — CLOSED.
- B-010 Call asset compliance + post-certification campaign review — OPEN; issue #110.
- B-011 Git branch reconciliation — CONTROLLED; enforce `main ⊆ dev` before/after production releases.
- B-012 Website visual/responsive development — PARTIAL / OPEN; issue #114. Real imagery refresh accepted; mobile/tablet navigation remains a known defect and additional site polish remains planned.
- B-013 Ad/asset policy readback — DATA_GAP; current connector can return zero rows while campaign-level reads work; do not infer approval.

---

## 6. Current priority queue — 2026-10-31

| Priority | Lane | Item | State / next evidence |
|---:|---|---|---|
| 0 | Release control | Promote validated real-image/site visual release + updated roadmap/handoff to `main` | ACTIVE / exact-head CI required |
| 1 | Google Ads / certification | Review Dr. Farah's new response and determine exact LegitScript / Google healthcare / call-asset next actions | NEXT |
| 2 | Google Ads | Re-read policy/review status of six RSAs + relevant assets when source surfaces them | DATA_GAP / retry without blocking |
| 3 | Google Ads | Resolve healthcare-safe call asset path under issue #110 | OPEN |
| 4 | Paid pilot | Final readiness review + explicit spend decision for local and/or traveler campaign | AFTER policy/certification/readiness review; no automatic enable |
| 5 | Website | Dedicated responsive navigation fix for mobile/tablet; continue visual/accessibility/performance polish | OPEN / important but not current Ads blocker unless landing usability is affected |
| 6 | Search/SEO | Monitor urgent-care + Pre-Op query movement and continue high-intent opportunity map | READY |
| 7 | GBP/local | Factual profile/service/reputation cleanup | READY |
| 8 | GA4 | Close safe live receipt/settings gaps | READY |
| 9 | Economics | Replace provisional assumptions with clinic economics/capacity | READY where inputs exist |
| 10 | Real conversion | First legitimate click→booking→completed visit→Google Ads import | IN-PILOT acceptance |
| 11 | AI Ads | Verify eligibility/account and design channel pilot | later lane |
| 12 | Partnerships/content | Traveler/pre-op partnerships and query-led content | READY where inputs exist |
| 13 | Growth Intelligence | Cross-channel dashboard/weekly decision loop | design can continue |

---

## 7. What must not block progress

Do not stop all growth work because one certification, policy/reporting field, exact margin, first paid conversion, future website polish task or AI channel dependency is pending. Document dependency + restart condition and continue the highest-value safe lane.

---

## 8. What must still block launch/spend/scale

Do not enable or materially scale paid traffic if production booking is unhealthy, attribution is known broken, landing intent is materially mismatched, policy prohibits delivery, outcome recording is duplicating/corrupting, explicit spend authorization is absent, capacity cannot absorb demand or economics are clearly unacceptable.

---

## 9. Resume protocol

Every substantive session:
1. read `PROJECT_HANDOFF.md` and this roadmap;
2. check exact `dev`/`main` heads and Jenkins state before Git writes;
3. check live systems for changed facts;
4. re-check hard blockers;
5. execute highest-value eligible work in parallel;
6. batch related code changes before CI;
7. record material evidence/results in GitHub/issues;
8. update handoff after material sessions.

No material project result should exist only in chat.
