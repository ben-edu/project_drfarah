# Dr. Farah VIP Urgent Care — Master Project Roadmap

> **Repository:** `ben-edu/project_drfarah`  
> **Canonical roadmap:** this file only  
> **Integration branch:** `dev`  
> **Production branch:** `main`  
> **GitHub:** durable project memory, code, roadmap, handoff, decisions and evidence  
> **OpenProject:** authoritative for live work-package status, assignee, dates, dependencies and milestones  
> **Live systems:** authoritative for their own current state  
> **Exact resume point:** `PROJECT_HANDOFF.md`

**Operating mode:** Growth Acceleration / parallel execution.  
**Roadmap refreshed:** 2026-10-29.

---

## 1. Mission

Build and operate one integrated growth system across Google Ads, Search Console, Google Business Profile, GA4, first-party attribution, completed-visit feedback, conversion-focused website/landing paths, service economics, ChatGPT Ads, traveler/hotel growth, pre-op referrals, physician-led content and Growth Intelligence.

The business outcome is completed visits and defensible economics, not clicks, impressions or superficial platform conversions alone.

---

## 2. Authority and control

When sources disagree, use this order:

1. current verified clinic/business fact from Dr. Farah or authoritative clinic record;
2. live production/account system for its own current state;
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

`PROJECT_HANDOFF.md` is the exact live resume point and must be updated after material sessions.

---

## 3. Execution rules — Growth Acceleration mode

1. **Parallel by default.** An external blocker in one lane does not stop safe independent work elsewhere.
2. **Production is the destination.** Validated work should move through normal release controls rather than remain indefinitely on `dev`.
3. **Develop more, build less.** Batch related changes before CI. Avoid redundant Jenkins jobs.
4. **Git discipline is mandatory.** Follow `docs/GIT_RELEASE_STRATEGY.md`: normal flow is `feature/fix/docs -> dev -> main`; current `main` must be contained in `dev` before normal promotion; production-only hotfixes/selective releases must be reconciled back into `dev` immediately.
5. **One measurement model.** Ads, Search Console, GBP, GA4, first-party attribution and website behavior are one acquisition system.
6. **Legacy evidence before cleanup.** Preserve useful historical evidence before archive/removal.
7. **Working assumptions are allowed.** Missing exact economics must not stall safe research/design; label provisional assumptions and replace them later.
8. **Completed visit is the primary business outcome.** Booking/call signals remain secondary/diagnostic.
9. **Privacy boundary.** Never send unnecessary patient PII/PHI, reason-for-visit or clinical context to marketing platforms.
10. **Real-data acceptance belongs in the pilot.** Tests that inherently require real traffic/events should not block all setup; hard-gate only production breakage, privacy/security, data integrity, policy prohibition or unauthorized spend.
11. **No silent defects.** Newly discovered issues must be fixed or durably tracked in roadmap/issues; do not simply work around and forget them.

---

## 4. Master gates — current state

| Gate | State | Current evidence / next requirement |
|---|---|---|
| G0 CONTROL PLANE | GREEN | GitHub roadmap + handoff + decisions + Git release strategy operational |
| G1 BOOKING HEALTHY | GREEN | booking incident resolved; no new regression |
| G2 MEASUREMENT READY | PARTIAL / PILOT-READY | Data Manager validate-only HTTP 200; first legitimate completed-visit live import/dedupe/reconciliation remains scale gate |
| G3 GOOGLE BASELINES | PARTIAL | Ads/GBP/Search Console captured; GA4 live receipt/settings soft validation remains |
| G4 FOUNDATION CORRECTED | PARTIAL | production landing/deployment path healthy; GBP/GA4/SEO improvement cycle continues |
| G5 ECONOMICS/PRIORITIES | PROVISIONAL | documented provisional pilot economics; authoritative clinic economics still desired |
| G6 LANDING PATHS | GREEN for current paid pilots | urgent-care + traveler paid landings production-deployed; traveler production `main/1` green |
| G7 LOCAL PAID EXPERIMENT | READY EXCEPT POLICY/LAUNCH AUTHORIZATION | local campaign PAUSED; geo live-readback = `PRESENCE`; final ad/asset policy readback + spend authorization before enable |
| G8 TRAVELER PAID EXPERIMENT | BUILT / PAUSED | campaign, 3 ad groups, 36 positives, 32 negatives, safe assets and 3 RSAs created; geo live-readback = `PRESENCE`; policy readback + spend authorization remain |
| G9 LOCAL GROWTH CYCLE | IN PROGRESS | GBP baseline exists; cleanup/reputation cadence remains |
| G10 AI PAID READY | WAITING_EXTERNAL | ChatGPT Ads account/eligibility not yet established |
| G11 PARTNERSHIP EXPERIMENTS | PLANNED / PARTIAL PREP | traveler/hotel and pre-op referral engines remain roadmap lanes |
| G12 CONTENT ENGINE | PLANNED | physician-led content system follows query/partner evidence |
| G13 GROWTH INTELLIGENCE / REPEATABLE CYCLE | PLANNED / PARTIAL FOUNDATION | source→appointment exists; completed-visit/cost/economics loop still maturing |

---

# Phase A — Measurement completion

### A1 — Data Manager technical acceptance

**DONE.** Real Google Data Manager `validateOnly=true` request returned HTTP 200 after API/auth/runtime ADC remediation. Do not fabricate a click ID or conversion.

### A2 — Production measurement promotion

**DONE.** Compatible Data Manager/attribution runtime batch was promoted to production through PR #104; subsequent production smoke recovery was completed through PR #105.

### A3 — First legitimate completed-visit acceptance

**IN PILOT / SCALE GATE.** On the first legitimate completed appointment carrying GCLID/WBRAID/GBRAID:
1. validate exact eligible row;
2. send one controlled `visit_completed` with explicit recording authorization;
3. replay the same deterministic transaction ID to verify dedupe/idempotency;
4. reconcile Google Ads to the internal completed appointment;
5. keep `Visit Completed` Secondary until trusted.

This does not block a small controlled pilot once its own launch gates are satisfied.

---

# Phase B — Google Ads growth system

## B1 — Legacy evidence / cleanup

- Legacy Smart campaign `22552983079` remains PAUSED; preserve forensic value and do not relaunch as primary acquisition.
- Google-managed Local Services campaign `23637947414` must not be altered without a specific decision; live system state is authoritative.

## B2 — Local urgent-care Search pilot

Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28`.

Current state:
- PAUSED; no authorized spend;
- Manual CPC;
- provisional configured budget $40/day;
- five-mile Beverly Hills targeting and clinic-hours schedule;
- Exact/Phrase positive keywords + negatives; no Broad;
- three PAUSED ad groups and three PAUSED RSAs;
- production landing `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`;
- live Windsor campaign read on 2026-10-29 confirms positive geo mode `PRESENCE`.

Ad groups:
1. `Urgent Care | Beverly Hills` — `196894367450` — $4.50 default CPC.
2. `Urgent Care | Near Me` — `204328258769` — $4.50 default CPC.
3. `Walk-In | Same-Day` — `199388744537` — $4.00 default CPC.

RSAs:
- `829832740743`
- `829881874987`
- `829963008380`

Keyword Planner evidence on 2026-10-29:
- `urgent care beverly hills`: ~1,000 average monthly searches, MEDIUM competition, historical average CPC ~$3.56, top-of-page range roughly $1.54–$7.58;
- this supports the current $4–$4.50 initial Manual CPC range directionally; do not change bids from planner data alone.

Next: obtain fresh ad/asset policy readback when the connector surfaces it; then controlled launch only with explicit spend authorization and existing finite guardrails. Review search terms early and optimize against completed visits/economics rather than CTR alone.

## B3 — Traveler / pre-arrival Search pilot

Campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`.

Current state:
- PAUSED; no authorized spend;
- Manual CPC;
- configured $20/day while PAUSED; configuration is not spend authorization;
- United States geo; English; 06:00–22:00 daily account-time schedule;
- EU political-ad declaration: No;
- live Windsor campaign read confirms `PRESENCE`;
- 36 Exact/Phrase positives;
- 32 campaign negatives for overlap/waste/policy control;
- dedicated production landing `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`;
- production `main/1` for traveler release is green.

PAUSED ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — $3.50 default CPC.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — $3.50 default CPC.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — $4.00 default CPC.

PAUSED RSAs:
- `829861283229`
- `829861321812`
- `829991120837`

Policy-safe campaign assets already created: four callouts, one structured snippet and four sitelinks. Call asset remains unresolved under issue #110.

Keyword Planner evidence:
- the ultra-specific traveler + Beverly Hills seeds returned no reportable monthly volume/CPC;
- `hotel doctor` and `doctor at hotel`: ~140 average monthly searches each across the US, LOW competition, historical average CPC ~$2.44;
- `doctor beverly hills`: ~260 searches but historical average CPC ~$27.01;
- `concierge doctor beverly hills`: ~590 searches and average CPC ~$10.72;
- `medical clinic beverly hills`: ~170 searches, LOW competition, average CPC ~$4.23.

DECISION — do not immediately broaden the traveler pilot into expensive generic `doctor beverly hills` / concierge traffic. Whole-US Presence targeting plus generic `hotel doctor` could also create nationwide waste without explicit Beverly Hills intent. Start precise; use real search-term/completed-visit evidence to decide controlled expansion.

## B4 — Google healthcare certification / policy remediation

FACT — `Clinic Services` sitelink asset `434419668405` pointing to `/services` is disapproved for `PRESCRIPTION_DRUG_SALE` with missing US certification and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete/hide the legitimate telemedicine/prescription-refill service merely to bypass policy.

Required sequence:
1. Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`.
2. After approval, complete Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services.
3. Re-read affected asset plus all ads/assets across both Search campaigns.
4. Preserve separate health-sensitive personalization restrictions; certification is not permission for prohibited health remarketing/Customer Match workarounds.

Current standard LegitScript pricing verified 2026-10-29: $975 non-refundable application fee + $2,150 annual certification after approval; standard first-year total $3,125.

Issue #106 tracks this external lane. Do not request/store portal passwords, payment details, PHI or patient records.

Site-readiness remains: replace draft `frontend/terms.html` and placeholder `frontend/notice-of-privacy-practices.html` with clinic/legal-approved content before final certification readiness.

## B5 — Call asset / mandatory post-certification review

Issue #110 tracks:
- healthcare/HIPAA-safe resolution of Google Call Ads Supplemental Terms / Communication Features;
- Google Support exclusion from monitoring/recording if the clinic/legal determination requires it;
- retry of the call asset only after that path is resolved;
- mandatory full post-certification review of both campaigns, ads, assets, policies and landing destinations.

Do not blindly accept recording terms. Call recording stays off unless clinic/legal explicitly approves.

Current connector limitation: campaign-level reads work, but current ad/asset policy reads may return zero rows even with `include_inactive`; forced refresh is unavailable on the connected TRIAL plan. Zero rows are a DATA_GAP, not approval.

---

# Phase C — Search Console / SEO / landing growth

Search Console property: `sc-domain:drfarahvipurgentcare.com`.

## C1 — Current 28-day opportunities

Recent first-party Search Console evidence on 2026-10-29:
- `dr farah vip urgent care`: 8 clicks / 57 impressions / CTR 14.04% / avg position 2.86;
- `dr farah clinic`: 4 / 5 / 80% / 1.2;
- `vip urgent care`: 2 / 95 / 2.11% / 1.16 — notable CTR opportunity despite top position;
- `beverly hills urgent care`: 25 impressions / position 11.68 / 0 clicks;
- `urgent care beverly hills`: 40 impressions / position 11.1 / 0 clicks;
- `urgent care near me`: 120 impressions / position 9.73 / 0 clicks;
- `urgent care`: 40 impressions / position 12.38 / 0 clicks;
- `urgent care beverly hills wilshire`: 39 impressions / position 21.26 / 0 clicks;
- `medical clearance for surgery near me`: 30 impressions / position 3.43 / 0 clicks;
- `medical clearance near me`: 9 impressions / position 1.56 / 0 clicks;
- `private urgent care`: 17 impressions / position 1.0 / 0 clicks;
- `fast uti care`: 27 impressions / position 6.93 / 0 clicks;
- `best executive physical in beverly hills`: 9 impressions / position 6.33 / 0 clicks.

Priority order:
1. improve urgent-care title/meta/on-page alignment and internal linking for near-page-one Beverly Hills/near-me intent;
2. improve Pre-Op snippet/on-page alignment for `medical clearance for surgery` because ranking is already strong but CTR is zero in the current sample;
3. inspect brand/VIP snippets where rank is high but CTR is weak;
4. use search data to inform later service/content work rather than optimizing every noisy one-impression query.

## C2 — Production indexing model

Source HTML intentionally uses `noindex,nofollow,noarchive` on general static pages for staging safety. `scripts/prepare-production-frontend.sh` removes noindex in production and swaps in `robots.production.txt`:

- `User-agent: *`
- `Allow: /`
- production sitemap declared.

Do not remove the staging noindex pattern from source as an SEO “fix”; production crawlability is assembled and tested during deployment.

`/book` and `/patient-registration` remain noindex and excluded from sitemap unless strategy changes explicitly.

## C3 — Current SEO implementation batch

Planned/active batch from 2026-10-29 evidence:
- tighten urgent-care title/meta and H1/lead toward Beverly Hills urgent-care intent without unsupported claims;
- tighten Pre-Op title/meta/H1 toward medical clearance for surgery;
- preserve current factual hours/prices/medical disclaimers;
- after release, monitor 28-day Search Console movement rather than expecting immediate ranking changes.

## C4 — IV / regenerative / weight-management search lanes

IV local terms currently rank poorly (~positions 45–70+), e.g. `iv therapy beverly hills`, `iv drip(s) beverly hills`. PRP local service terms also rank poorly while informational cost/comparison content performs materially better. Weight-management terms currently rank poorly (~48–62).

These are longer-term content/landing opportunities, not faster wins than urgent care and Pre-Op. Any healthcare/prescription-related paid use remains subject to policy/certification.

---

# Phase D — Website image quality / performance

Issue #114 is the durable image-quality work item.

Current approved native dimensions:
- `home-hero-doctor.webp`: 800×450 — limited for full-screen/retina desktop hero;
- `dr-farah-portrait.webp`: 520×650 — potentially adequate at moderate width; verify visually;
- `dr-farah-clinic.webp`: 800×533;
- `clinic-exterior.webp`: 480×320 — low for large feature use;
- `service-iv-treatment.webp`: 500×281 — known P0 quality defect on Services/IV large hero;
- traveler/pre-op/virtual service assets: 800×450.

Rules:
- do not fabricate Dr. Farah/clinic imagery;
- do not restore retired generic assets merely because they are larger;
- do not claim naive upscaling restores lost detail;
- obtain clinic-approved high-resolution originals, with IV first, then homepage hero and clinic exterior;
- after originals arrive, produce responsive derivatives, correct intrinsic dimensions, `srcset`/`sizes` where useful, high-priority LCP behavior for hero, lazy/deferred loading below fold, and desktop/mobile visual QA.

This work is independent of LegitScript. Source-image replacement waits only on the real high-resolution originals.

---

# Phase E — Google Business Profile / Maps / reputation

Current GBP location `locations/6719840585856592244`; primary category `Urgent care center`; captured baseline 5.0 / 109 reviews.

E1 validate regular/special hours, address/map pin, phone, website/booking links and categories.

E2 evaluate service catalogue selectively for factual availability, duplication, strategic priority, claims/pricing and website alignment; do not bulk-delete merely because the list is large.

E3 establish privacy-safe neutral review request/response cadence and issue escalation.

E4 maintain factual local competitor loop based on visibility, category, reviews, hours, messaging and booking experience.

---

# Phase F — GA4 / cross-channel measurement quality

GA4 production property `489069776`; Web Stream `11211773871`; Measurement ID `G-D58FTMF05S`.

Soft validation remains:
- safe Realtime/DebugView controlled event on allowlisted low-risk page;
- timezone/currency;
- Enhanced Measurement;
- consent behavior;
- selected-page allowlist;
- excluded health-intent/sensitive-page verification.

Roles stay distinct:
- GA4 = behavioral/diagnostic analysis on approved low-risk surfaces;
- first-party database = source/click→appointment linkage;
- Google Ads offline conversion = optimization feedback;
- Search Console = organic search truth;
- GBP = Maps/profile truth.

---

# Phase G — Controlled paid experiment / optimization cycle

Launch only when the campaign-specific minimum gates are satisfied.

Each pilot needs:
- named hypothesis;
- exact intent/geography;
- finite learning budget and hard spend ceiling;
- controlled keywords/match types/negatives;
- relevant production landing page;
- completed-visit linkage;
- secondary booking/call diagnostics;
- stop/modify/scale thresholds;
- review date.

Search-term waste control begins early. Scale only on completed visits, defensible CAC/contribution, capacity and measurement confidence.

Do not enable either current Search campaign until explicit launch/spend authorization is present and final core policy/readiness review is acceptable.

---

# Phase H — Stable offline conversion operations

After the first controlled real conversion succeeds:
- identify eligible new `visit_completed` rows with click IDs;
- record import state/idempotency;
- batch safely;
- retry transient failures with bounded backoff;
- quarantine permanent/schema/auth failures;
- never print click IDs or patient data in routine logs;
- expose non-sensitive health/metrics;
- alert on sustained failures;
- reconcile imports to Google Ads periodically.

This is operational automation, not autonomous marketing spend.

---

# Phase I — AI / ChatGPT Ads paid channel

Treat as a real future paid-acquisition workstream.

I1 verify current healthcare eligibility, policy and account access before spend.

I2 if eligible, define incremental hypothesis versus Google Search, including local care discovery, traveler/VIP use cases and other policy-permitted intents.

I3 use dedicated source/UTM/first-party attribution and completed-visit outcome where technically/policy-compliantly possible.

I4 create only a finite-budget pilot with explicit stop/scale rules.

Current facts: ChatGPT Ads Manager is installed; prior account discovery found no accessible clinic ad account; Windsor exposes `openai_ads` but no account is connected. This lane may proceed once final Google launch configuration is stable and need not wait for long-term Google learning where independent.

---

# Phase J — Service economics and capacity

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

---

# Phase K — Traveler / hotel / VIP partnership growth

Preserve sequence:
- traveler baseline;
- existing hotel/concierge sources;
- target list;
- accurate service scope/response model;
- partner interviews;
- partner kit;
- attribution;
- small pilot;
- completed-visit/revenue/repeat-referral review.

No unsupported 24/7, mobile or response-time promise.

The paid traveler Search pilot in Phase B is a separate acquisition experiment and can inform this partnership lane, but does not replace it.

---

# Phase L — Pre-Op referral engine

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

Search Console already shows high organic visibility for medical-clearance queries; use this evidence to improve the patient-facing page while the B2B referral engine is developed separately.

---

# Phase M — Physician-led content / creative

Content priorities must be fed by Search Console, Ads search terms, GBP/reviews, traveler/pre-op questions, website friction and service economics.

Build reusable long-form + short-form + website + paid creative derivatives. Measure qualified business contribution, not views alone.

---

# Phase N — Growth Intelligence and recurring operating cycle

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

The Growth Intelligence layer is not an EHR and must not become one.

---

## 5. Preserved OpenProject work-package identifiers

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

## 6. Durable blockers / tracked issues

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — SCALE GATE only: first legitimate live completed-visit import + replay/dedupe + reconciliation.
- B-003 Local paid destination — CLOSED.
- B-004 Local campaign geo — CLOSED with live connector readback `PRESENCE`.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 authoritative clinic economics/capacity — SOFT.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL.
- B-008 LegitScript + Google healthcare certification — WAITING_EXTERNAL / HIGH PRIORITY; issue #106; independent work continues.
- B-009 Traveler landing production readiness — CLOSED; production `main/1` green.
- B-010 Call asset compliance + post-certification campaign review — OPEN; issue #110.
- B-011 Git branch reconciliation — CLOSED; `main` is ancestor of current `dev`; `dev/31` SUCCESS on `085df28a6488587bae94bd1400553b8750091555`.
- B-012 Image-quality remediation — OPEN; issue #114; real high-resolution clinic originals required for material sharpness gains on IV/hero/exterior.
- B-013 Ad/asset policy readback — DATA_GAP; current Windsor ad/asset-level reads return zero rows while campaign-level reads work; do not treat as approval.

---

## 7. Current parallel priority queue — 2026-10-29

| Priority | Lane | Item | State / next evidence |
|---:|---|---|---|
| 0 | Website/Search | Ship evidence-led urgent-care + Pre-Op SEO snippet/on-page improvements as one CI batch | READY / ACTIVE |
| 1 | Google Ads | Re-read policy/review status of all six RSAs + campaign assets when live reporting surfaces them | DATA_GAP / RETRY WITHOUT BLOCKING OTHER LANES |
| 2 | Google Ads | Resolve healthcare-safe call asset path under issue #110 | WAITING for clinic legal/HIPAA determination + Google Support path |
| 3 | Healthcare certification | Dr. Farah completes LegitScript; then Google healthcare certification | WAITING_EXTERNAL / issue #106 |
| 4 | Image quality | Obtain high-resolution approved IV, homepage hero and clinic exterior originals; then responsive optimization | WAITING for source files / issue #114 |
| 5 | Search/SEO | Monitor urgent-care + Pre-Op query movement and continue high-intent opportunity map | READY NOW |
| 6 | GBP/local | Audit factual profile/service/reputation opportunities | READY NOW |
| 7 | GA4 | Close safe live receipt/settings baseline gaps | READY NOW |
| 8 | Economics | Replace provisional assumptions with clinic economics/capacity as available | READY where inputs exist |
| 9 | Paid pilot | Final readiness review + explicit spend decision for local and/or traveler campaign | AFTER policy readback; no automatic enable |
| 10 | Real conversion | First legitimate click→booking→completed visit→Google Ads import | IN-PILOT acceptance after traffic exists |
| 11 | AI Ads | Verify eligibility/account and design channel pilot | READY after final Google launch configuration stable |
| 12 | Traveler/pre-op partnerships/content | Advance independent baselines, referral/partner materials and query-led content | READY where inputs exist |
| 13 | Growth Intelligence | Cross-channel dashboard/weekly decision loop | design can continue; full loop follows stable outcome/cost data |

---

## 8. What must not block progress

Do not stop all growth work because:
- LegitScript is waiting on Dr. Farah;
- one Google policy/reporting field is delayed;
- exact clinic margin is not yet available;
- the first real paid conversion has not happened;
- a high-resolution image source has not yet arrived;
- an AI ad channel is awaiting eligibility/account access.

Document the dependency, preserve the restart condition and continue the highest-value safe independent lane.

---

## 9. What must still block launch/spend/scale

Do not enable or materially scale paid traffic when any of these are true:
- production booking is unhealthy;
- attribution is known broken;
- landing intent is materially mismatched;
- campaign/ad policy prohibits delivery;
- conversion recording is duplicating/corrupting outcomes;
- the exact paid launch/spend action is not authorized;
- clinic capacity cannot absorb expected demand;
- economics are clearly unacceptable.

A small controlled learning experiment can proceed once its own minimum safety/measurement/policy dependencies are satisfied; scale requires stronger completed-visit evidence.

---

## 10. Resume protocol

Every substantive session:
1. read `PROJECT_HANDOFF.md`;
2. read this priority queue and relevant lane;
3. check exact `dev`/`main` heads, lineage and Jenkins state before Git/release work;
4. check live systems for facts that may have changed;
5. re-check HARD blockers;
6. execute the highest-value eligible work in parallel lanes;
7. batch related code changes before CI/build;
8. record material evidence/results in GitHub/issues;
9. update `PROJECT_HANDOFF.md` before ending.

No material project result should exist only in chat.
