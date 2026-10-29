# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** Continue from this file + `ROADMAP.md`; live systems remain authoritative for their own state.

**Last updated:** 2026-10-29  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 1. Operating model

Growth Acceleration / parallel execution. Independent safe lanes continue while external dependencies wait. Hard-gate only production breakage, privacy/security, data integrity, policy prohibition or unauthorized spend. Tests that inherently require real traffic belong inside the controlled pilot. Optimize toward completed visits and defensible economics, not superficial conversions.

Never send unnecessary patient PII/PHI, reason-for-visit or clinical content to marketing systems.

User-facing project explanations default to Persian script; explain the Persian concept first and use exact English UI labels only when useful.

Git/release control follows `docs/GIT_RELEASE_STRATEGY.md`: normal flow is `feature/fix/docs -> dev -> main`; current `main` must be contained in `dev` before normal promotion; production-only exceptions must be reconciled back into `dev` immediately. CI queue guard: do not create redundant branches/PRs/commits while a relevant Jenkins build is running.

---

## 2. Branch / deployment state

FACT — production `main` is `9cb6b0def117a9f1863a37216fd8460b47a220be`; Jenkins `main/1` SUCCESS. This production release includes the policy-safe traveler landing at `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

FACT — current `dev` is reconciliation commit `085df28a6488587bae94bd1400553b8750091555`; Jenkins `dev/31` SUCCESS.

FACT — branch reconciliation is complete: current `main` is an ancestor of `dev` (`behind_by=0`). PR #112 and PR #113 were closed/superseded; stale `pr-head` pending statuses from those closed PRs are not valid active branch builds.

DECISION — do not return to selective production reconstruction as the normal release method. Normal release path is coherent validated `dev -> main`.

---

## 3. Booking / first-party attribution / completed outcome

`G1-BOOKING-HEALTHY`: GREEN unless a new regression appears.

Production supports source/UTM, GCLID/GBRAID/WBRAID, opaque marketing session ID, first/last-touch context and partner/traveler markers. `appointment_attributions` is 1:1 and persisted atomically with booking. Marketing attribution excludes page path, service, reason-for-visit, patient PII and clinical content.

`visit_completed`: authoritative appointment status `completed`; deterministic transaction key `visit_completed:<appointment_id>`; occurrence time `starts_at`; non-clinical attribution only.

Google Data Manager validate-only acceptance is complete: a real request returned HTTP 200. First legitimate completed paid visit remains the live recording + replay/dedupe + reconciliation acceptance. Keep `Visit Completed` Secondary until that passes.

---

## 4. Local Google Search pilot

Google Ads customer `652-510-3588`.

Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28` — PAUSED. Manual CPC, provisional configured $40/day, five-mile Beverly Hills targeting, clinic-hours schedule, Exact/Phrase positives and negatives, three PAUSED ad groups and three PAUSED RSAs.

Ad groups:
1. `Urgent Care | Beverly Hills` — `196894367450` — $4.50 default CPC.
2. `Urgent Care | Near Me` — `204328258769` — $4.50 default CPC.
3. `Walk-In | Same-Day` — `199388744537` — $4.00 default CPC.

RSAs: `829832740743`, `829881874987`, `829963008380`.

FACT — live Windsor campaign read now confirms positive geo mode `PRESENCE`; the old geo readback gate is closed.

Keyword Planner: `urgent care beverly hills` ~1,000 average monthly searches, MEDIUM competition, historical average CPC ~$3.56; current initial Manual CPC range is directionally reasonable. Do not change bids from planner data alone.

Production landing: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

NEXT — obtain fresh ad/asset policy readback when available; do not enable/spend without explicit launch authorization.

---

## 5. Traveler / pre-arrival Google Search pilot

Campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29` — PAUSED. Manual CPC, configured $20/day while paused (not spend authorization), US geography, English, 06:00–22:00 schedule, EU political-ad declaration No.

PAUSED ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — $3.50 default CPC.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — $3.50 default CPC.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — $4.00 default CPC.

FACT — 36 Exact/Phrase positives and 32 campaign-level negatives exist. The negatives control local overlap, emergency/hospital waste, jobs/training, dental/vet, free/cheap, certification-sensitive prescription/refill/telemedicine/virtual intent and unrelated treatments.

FACT — live Windsor campaign read confirms `PRESENCE`.

FACT — policy-safe campaign assets created: four callouts, one structured snippet and four sitelinks.

FACT — three PAUSED traveler RSAs created against the dedicated production landing:
- `829861283229`
- `829861321812`
- `829991120837`

Landing: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`; production `main/1` green.

Keyword Planner: ultra-specific traveler+Beverly Hills seeds had no reportable volume. Broader evidence: `hotel doctor` / `doctor at hotel` ~140 US searches each and historical CPC ~$2.44; `doctor beverly hills` ~260 but ~$27 historical CPC; `concierge doctor beverly hills` ~590 and ~$10.72. DECISION — do not broaden blindly; start precise and use actual search-term/completed-visit evidence.

DATA_GAP — Windsor currently returns no rows for ad-level/asset-level policy reads even with `include_inactive`; campaign-level reads work. Forced refresh is unavailable on the connected TRIAL plan. Zero rows are not evidence of approval.

---

## 6. Google healthcare policy / LegitScript

FACT — `Clinic Services` sitelink asset `434419668405` pointing to `/services` is DISAPPROVED for `PRESCRIPTION_DRUG_SALE` with missing certification for the United States and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete/hide the legitimate service to bypass policy.

Correct path: Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`; after approval, complete Google healthcare certification for child account `652-510-3588`, US telemedicine/prescription-drug services. Issue #106 tracks this.

WAITING_EXTERNAL — Dr. Farah application/payment/approval. Do not request portal passwords, payment details, PHI or patient records.

FACT — standard LegitScript pricing verified 2026-10-29: $975 non-refundable application fee + $2,150 annual certification after approval; standard first-year total $3,125.

SITE READINESS GAP — `frontend/terms.html` remains draft/pending legal review and `frontend/notice-of-privacy-practices.html` remains a placeholder. Clinic/legal-approved content is required before final certification readiness.

Certification does not remove Google's separate health-sensitive personalization restrictions.

---

## 7. Call asset / mandatory post-certification review

Issue #110 is OPEN.

Attempted Google Ads call asset for `310-467-0101` was rejected because the account has not completed the Call Ads Supplemental Terms/compliance path.

Do not blindly accept call-recording terms for a healthcare advertiser. Clinic/legal must confirm the applicable HIPAA Covered Entity / Business Associate status for this use. If applicable, request Google Support exclusion from monitoring/recording before retrying the call asset. Call recording remains off unless clinic/legal explicitly approves.

Issue #110 also mandates a full post-certification review of both campaigns, all ads/assets, policies and landing destinations after LegitScript + Google healthcare certification. Do not close it early.

---

## 8. Search / website growth evidence

Search Console property: `sc-domain:drfarahvipurgentcare.com`.

High-priority 28-day evidence:
- `beverly hills urgent care`: 25 impressions, avg position 11.68, 0 clicks;
- `urgent care beverly hills`: 40 impressions, avg position 11.1, 0 clicks;
- `urgent care near me`: 120 impressions, avg position 9.73, 0 clicks;
- `urgent care beverly hills wilshire`: 39 impressions, avg position 21.26, 0 clicks;
- `medical clearance for surgery near me`: 30 impressions, avg position 3.43, 0 clicks;
- `medical clearance near me`: 9 impressions, avg position 1.56, 0 clicks;
- `vip urgent care`: 95 impressions, avg position 1.16, CTR 2.11%.

DECISION — prioritize evidence-led urgent-care and Pre-Op title/meta/on-page improvements before lower-ranking IV/PRP/weight-loss SEO work.

Production indexing architecture is intentional: source/staging pages may contain `noindex`; `scripts/prepare-production-frontend.sh` removes it for production and installs `robots.production.txt` with crawl allow + sitemap. Do not remove staging noindex as an SEO fix.

---

## 9. Image-quality work

Issue #114 is OPEN and independent of LegitScript.

Current native dimensions:
- homepage hero `home-hero-doctor.webp`: 800×450;
- Dr. Farah portrait: 520×650;
- clinic interior: 800×533;
- clinic exterior: 480×320;
- IV hero: 500×281;
- traveler/pre-op/virtual service images: 800×450.

P0 — replace the 500×281 IV hero with a clinic-approved higher-resolution original. Next: higher-resolution homepage hero and clinic exterior where available. Do not fabricate Dr. Farah/clinic imagery, restore retired generic placeholders merely because they are larger, or present naive upscaling as recovered detail.

After originals arrive: generate responsive derivatives, use correct intrinsic dimensions / `srcset` / `sizes` where useful, prioritize LCP hero appropriately, lazy/defer below-fold images and visually validate desktop/mobile.

---

## 10. GBP / GA4 / AI Ads

GBP location `locations/6719840585856592244`; primary category Urgent care center; captured baseline 5.0 / 109 reviews. Core cleanup/reputation cadence remains open.

GA4 property `489069776`, stream `11211773871`, measurement `G-D58FTMF05S`. Safe public-page allowlist remains intentional; sensitive health-intent landings remain outside current GA4 allowlist. Soft live receipt/settings validation remains.

ChatGPT Ads remains a later paid-growth lane. Ads Manager installed; prior discovery found no accessible clinic ad account; Windsor `openai_ads` has no connected account. Begin eligibility/account work after final Google launch configuration is stable; no spend without policy/measurement/budget gates.

---

## 11. Current blockers / gates

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — SCALE GATE only: first legitimate live completed-visit import + replay/dedupe + reconciliation.
- B-003 Local paid destination — CLOSED.
- B-004 Local campaign geo — CLOSED; live readback `PRESENCE`.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 authoritative clinic economics/capacity — SOFT.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL.
- B-008 LegitScript + Google healthcare certification — WAITING_EXTERNAL / HIGH PRIORITY; issue #106; independent work continues.
- B-009 Traveler landing production readiness — CLOSED; `main/1` SUCCESS.
- B-010 Call asset compliance/post-cert review — OPEN; issue #110.
- B-011 Git branch reconciliation — CLOSED; `main` contained in `dev`; `dev/31` SUCCESS.
- B-012 Image quality — OPEN; issue #114; high-resolution approved source files required for material sharpness improvement.
- B-013 Ad/asset policy readback — DATA_GAP; current connector returns zero ad/asset rows; do not infer approval.

---

## 12. Exact next actions

1. Complete one evidence-led SEO batch for urgent-care + Pre-Op pages; keep claims/facts/prices unchanged except wording alignment; validate exact candidate SHA in Jenkins before integration.
2. Restore the durable long-term phases accidentally omitted from the shortened roadmap; preserve service economics, traveler/hotel partnerships, pre-op referral engine, content engine, Growth Intelligence and verified OpenProject IDs.
3. Recheck all six RSA and relevant asset policy/review statuses when a fresh ad-level source becomes available; do not block independent work on the current Windsor read gap.
4. Resolve issue #110 call-asset path after clinic legal/HIPAA determination and Google Support handling; full post-cert review remains mandatory.
5. Dr. Farah continues LegitScript issue #106. After approval, complete Google healthcare certification and re-read affected policy objects.
6. Obtain clinic-approved high-resolution image originals for issue #114, beginning with IV, homepage hero and clinic exterior; then implement responsive delivery/visual QA.
7. Continue GBP factual cleanup/reputation and GA4 soft validation in parallel.
8. First legitimate paid completed visit → Data Manager live import + replay/dedupe + reconciliation; keep `Visit Completed` Secondary until passed.
9. Once policy/readiness is acceptable, present a controlled launch decision for the local and/or traveler pilot. Do not enable or incur spend without explicit authorization.
10. Begin ChatGPT Ads eligibility/account lane after final Google launch configuration is stable.

---

## 13. Resume protocol

Read this file, then `ROADMAP.md`; check exact `dev`, `main`, Jenkins statuses, branch lineage and live Ads state. Before any Git write that can trigger CI, verify no relevant build is already pending/running. Before production promotion, enforce `docs/GIT_RELEASE_STRATEGY.md`. Preserve spend/privacy/data/policy hard gates. Continue safe independent lanes instead of waiting on external certification or campaign-data-dependent tests. Never recreate existing campaign/ad objects without live read-back. Update this handoff after material sessions and keep deferred work in `ROADMAP.md`/issues.
