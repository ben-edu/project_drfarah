# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** Continue from this file + `ROADMAP.md`; live systems remain authoritative for their own state.

**Last updated:** 2026-10-29  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 1. Operating model

Growth Acceleration / parallel execution. Independent safe lanes continue in parallel. Production is the destination for validated work. Use risk-based gates: block only for production breakage, privacy/security, data integrity, or unauthorized spend; acceptance that requires real campaign data belongs inside the controlled pilot. Optimize toward completed visits, not superficial platform conversions. Never send unnecessary patient PII/PHI/clinical context to marketing systems.

---

## 2. Branch / deployment state

FACT — `dev` head `c07b580b00adad3891d8924900700b52ccec1788`; Jenkins `dev/26` SUCCESS.

FACT — integrated growth/measurement batch was promoted through PR #104. Production initially reached `fcc8d855eff53e25f27673b53a2e94a0e37efd49`; `main/3` failed only on stale frontend redirect smoke expectations after the frontend had already published.

FACT — recovery PR #105 updated only `Jenkinsfile` expectations for the intentional urgent-care redirects and added direct smoke coverage for `/urgent-care-beverly-hills`. Current production `main` is `5e34eea5ca5c1b78a0aeceb2a4fa287b7b15e1ae`; Jenkins `main/4` SUCCESS.

DECISION — do not roll back the urgent-care landing/redirect release. The CI expectation was stale; the intended redirect target is the new canonical landing page.

---

## 3. Booking / first-party attribution / completed outcome

`G1-BOOKING-HEALTHY`: GREEN unless a new regression appears.

Production supports source/UTM, GCLID/GBRAID/WBRAID, opaque marketing session ID, first/last-touch context and partner/traveler markers. `appointment_attributions` is 1:1 and persisted atomically with booking. Marketing attribution excludes page path, service, reason-for-visit, patient PII and clinical content.

`visit_completed` contract: authoritative appointment status `completed`; deterministic transaction key `visit_completed:<appointment_id>`; occurrence time `starts_at`; non-clinical attribution only.

---

## 4. Google Data Manager / completed-visit import

Google Ads customer `652-510-3588`. Conversion action `Visit Completed`, UI/action ID `7879009165`: Secondary, Converted leads, no value, Import from clicks, count One, 30-day click window, Data-driven attribution.

FACT — Google-side setup and API validation are complete. Issue #94 evidence records a real Data Manager request with `validateOnly=true` returning HTTP 200 after the runtime ADC mount/readability fix. Customer/destination/API/auth setup is therefore no longer the blocker.

FACT — the Data Manager implementation is now included in the production batch promoted through PR #104 and production `main/4` is green.

DATA_GAP — at validation time there was no legitimate completed visit carrying GCLID/WBRAID/GBRAID. Do not fabricate one.

DECISION — the first real eligible paid completed visit is the live acceptance test: send one controlled import with explicit recording authorization, replay the same transaction ID to verify dedupe/idempotency, then reconcile Google Ads to the internal completed appointment. Keep `Visit Completed` Secondary until this passes. This acceptance blocks scaling/primary-conversion promotion, not a small controlled pilot.

`G2-MEASUREMENT-READY`: PARTIAL / pilot-ready, scale acceptance pending first legitimate completed-visit import and reconciliation.

---

## 5. Google Ads — live current state

Customer `652-510-3588`, USD, America/Los_Angeles. Auto-tagging enabled.

Legacy Smart campaign `22552983079` remains PAUSED; do not relaunch as primary growth vehicle. System Local Services campaign `23637947414` remains effectively paused; leave unchanged pending role clarification.

New Search pilot campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28` — remains PAUSED with no authorized spend. Manual CPC, provisional $40/day, English, five-mile proximity around 34.067/-118.3934, clinic-hours schedule. Ad groups remain paused:

1. `Urgent Care | Beverly Hills` — `196894367450`, default CPC $4.50.
2. `Urgent Care | Near Me` — `204328258769`, default CPC $4.50.
3. `Walk-In | Same-Day` — `199388744537`, default CPC $4.00.

18 initial positive keywords are Exact/Phrase only; initial campaign negatives cover 24-hour/24-7, ER/hospital-emergency, free-clinic, job/career/training, veterinary and dental intent. Existing assets include clinic call asset, callouts and sitelinks.

FACT — after production `main/4` turned green, three Responsive Search Ads were created PAUSED against the production landing URL; they cannot spend while paused:

- ad `196894367450~829832740743` — `RSA | Urgent Care Beverly Hills | v1`;
- ad `204328258769~829881874987` — `RSA | Urgent Care Near Me | v1`;
- ad `199388744537~829963008380` — `RSA | Walk-In Same-Day | v1`.

All use `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`. One initial same-day RSA write was rejected because a description exceeded 90 characters; copy was shortened and the retry succeeded. No duplicate successful ad was created by that rejected attempt.

BLOCKER B-004 — positive geo option remains `PRESENCE_OR_INTEREST` per last verified read-back. It must be changed to Presence-only (`people in or regularly in the targeted locations`) before campaign enable. Windsor's available geo write action controls locations/proximities but does not expose the positive-geo-type switch. Do not enable campaign/ad groups/ads until this is fixed and read back.

---

## 6. Paid + organic landing path

Canonical production URL: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

The production release includes the landing page, sitemap entry, and intentional redirects `/urgent-care-near-you` and `/vip-urgent-care` to the canonical landing. Production Jenkins `main/4` directly smoke-tests the landing and corrected redirect expectations and is SUCCESS.

Landing design: Beverly Hills urgent-care intent, actual phone/address/hours, same-day only `when available`, book + call CTAs, 911/not-emergency-department language, `MedicalClinic` schema, existing first-party attribution via `app.js`, no GA4 injection under current health/privacy allowlist.

`G6-LANDING-PATHS-READY`: GREEN for the first Search pilot, subject to normal live monitoring.

---

## 7. Search Console / GBP / GA4

Search Console property `sc-domain:drfarahvipurgentcare.com`; captured 90-day baseline ~32,325 impressions, 308 clicks, CTR ~0.95%, average position ~11.8. Local query opportunities include urgent-care near-me/Beverly Hills terms around positions 10–16. Continue post-release indexing/canonical monitoring.

GBP location `locations/6719840585856592244`; primary category Urgent care center; captured baseline 5.0 / 109 reviews; regular hours Mon–Thu 08:30–17:30, Fri 08:30–16:30, weekends closed. Open cleanup: inspect Google updates, stale special hours, duplicate/aggressive service catalogue entries.

GA4 production property `489069776`, stream `11211773871`, measurement ID `G-D58FTMF05S`. Selected low-risk public-page architecture remains intentional; sensitive booking/registration/service/treatment/admin surfaces excluded. Open soft validation: Realtime/settings/consent/excluded-page checks. New urgent-care landing remains outside GA4 allowlist; paid attribution uses first-party attribution + completed-visit feedback.

---

## 8. AI / ChatGPT Ads

Active later paid-growth lane. ChatGPT Ads Manager is installed but prior check returned no accessible clinic ad account. Windsor supports an `openai_ads` connector but it is not currently connected. Do not claim eligibility/onboarding yet. Issue #92 remains durable evaluation context. Start account/eligibility/onboarding work after the Google Search pilot's hard launch configuration is complete; do not wait for long-term Google scale learning to begin eligibility work.

---

## 9. Current blockers

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — PARTIAL / SCALE GATE. `validateOnly` HTTP 200 and production promotion complete; first legitimate paid completed-visit import + dedupe + reconciliation still required.
- B-003 Search pilot destination — CLOSED. Production landing/redirect smoke is green and paused RSAs now exist.
- B-004 Google Ads geo positive-location option — HARD LAUNCH GATE. Must become `PRESENCE`, not `PRESENCE_OR_INTEREST`.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 exact clinic economics — SOFT; use explicit provisional assumptions.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL until eligibility/onboarding path is completed.

---

## 10. Exact next actions

1. Keep campaign `24414014329`, all three ad groups and all three RSAs PAUSED.
2. Fix B-004 through a supported Google Ads UI/API path and read back Presence-only before any enable action. Do not substitute radius targeting for this setting.
3. After B-004 is verified, perform final campaign/ad/policy read-back and launch only within the already-approved controlled pilot budget/guardrails; do not materially increase spend without new authorization.
4. During the pilot, use the first legitimate Google-click completed visit for the controlled Data Manager recording + replay/dedupe + reconciliation acceptance. Keep `Visit Completed` Secondary until passed.
5. Review search terms early, add negatives aggressively, and judge toward completed visits/economics rather than clicks alone.
6. In parallel, continue GBP cleanup, Search Console post-release monitoring and GA4 soft validation.
7. Begin ChatGPT Ads eligibility/account-onboarding investigation once B-004/final Google launch configuration is complete; any ChatGPT pilot requires finite budget, dedicated source attribution and stop/scale rules.

---

## 11. Resume protocol

Read this file, then `ROADMAP.md`; check `dev`, `main`, exact Jenkins statuses and live Ads state. Preserve the hard spend/privacy/data gates above. Continue safe independent lanes instead of waiting on campaign-data-dependent tests. Update this handoff after every material session and put durable deferred work/blockers in `ROADMAP.md`.