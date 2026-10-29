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

User-facing project explanations should default to Persian script. Use clear Persian equivalents first; include exact English UI labels only when they help the user find a setting.

---

## 2. Branch / deployment state

FACT — current `dev` head is `d31807e929f725e6ab35b432c8cdbed03bc52047`; Jenkins `dev/28` SUCCESS.

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

FACT — on 2026-10-29 the user changed the campaign positive location option in the Google Ads UI to Presence-only (`people in or regularly in the targeted locations`).

DATA_GAP — the connected Windsor read is currently cached and still reports the previous `PRESENCE_OR_INTEREST`; the current plan does not permit forced refresh. Treat the UI save as the latest direct evidence, but require a fresh Google/Windsor read-back before enable so B-004 can be closed with system evidence.

DECISION — keep this first urgent-care campaign Presence-only. Do not use it to capture pre-arrival travelers outside the area. Traveler/pre-arrival demand gets a separate campaign so local urgent intent and travel-planning intent can be measured and controlled independently.

---

## 6. Google Ads healthcare policy / LegitScript

FACT — the sitelink asset `Clinic Services` pointing to `https://drfarahvipurgentcare.com/services` is DISAPPROVED for `PRESCRIPTION_DRUG_SALE` with a missing-certification condition for the United States. It also carries `HEALTH_IN_PERSONALIZED_ADS` as a limited policy topic.

FACT — the classification is plausible because `/services` legitimately describes virtual urgent care / travel prescription refills. Do not solve this by deleting the service or hiding the business model.

DECISION — correct path is full certification: Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`; after approval, complete Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services. Issue #106 is the durable certification work item.

WAITING_EXTERNAL — Dr. Farah must decide whether to proceed with LegitScript and, if proceeding, complete the application/payment and provide the resulting approval/certificate/reference. Do not request portal passwords, payment details, PHI, patient records or other secrets in chat/repo.

FACT — current standard LegitScript pricing verified 2026-10-29: $975 non-refundable application fee per website; $2,150 annual certification fee per website after approval; standard first-year total $3,125. Optional expedited review is separate and not required.

SITE READINESS GAP — `frontend/terms.html` still states it is a draft pending legal review, and `frontend/notice-of-privacy-practices.html` is still a placeholder. Before certification submission/final review, replace both with clinic/legal-approved content. We can prepare implementation/drafts, but clinic facts and final approval must come from Dr. Farah/legal counsel.

IMPORTANT — certification can resolve the prescription-drug-services certificate problem, but it does not remove Google's separate health-sensitive personalization restrictions. Do not use restricted health remarketing/Customer Match workarounds. Search keywords, location targeting and allowed Google-defined targeting remain available subject to policy.

---

## 7. Second Google Search campaign — traveler / pre-arrival growth

DECISION — prioritize a separate paused Search campaign for travelers planning care in Beverly Hills before arrival. This is not a replacement for the local urgent-care pilot; it is a distinct acquisition hypothesis with separate budget, search terms, landing experience and measurement.

Working name: `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot`.

Initial strategy:
- objective: capture high-intent travelers/visitors who are outside Beverly Hills now but are explicitly planning medical access in Beverly Hills;
- initial geography: United States Presence-only at the broader source-market level, not Beverly Hills `Presence or interest`; rely on explicit Beverly Hills + traveler/visitor/hotel intent in keywords rather than Google's broad interest inference;
- match control: Exact/Phrase first; no broad match until completed-visit evidence supports expansion;
- intent themes: Beverly Hills doctor for travelers/tourists/visitors, doctor near Beverly Hills hotel, traveler medical care Beverly Hills, urgent care for visitors in Beverly Hills, hotel physician/medical care where accurately supported;
- landing: dedicated traveler/hotel care path with clear in-person/mobile availability, booking/call CTA, service-area/hours, no guarantee language, 911/not-ER language;
- policy split: in-person/pre-arrival traveler care can be prepared independently; any ad copy/landing claims about telemedicine prescribing/refills remain gated by LegitScript + Google healthcare certification;
- measurement: dedicated UTM/source naming, first-party click ID capture and completed-visit feedback exactly like the local pilot;
- overlap control: use traveler-specific modifiers and search-term negatives so pre-arrival planning does not contaminate the local urgent-care campaign; refine source markets from actual query/completed-visit evidence rather than assumptions;
- budget: create/configure PAUSED first. No new paid spend until the campaign budget is explicitly authorized under roadmap/spend rules.

HIGH PRIORITY — build the campaign architecture/keyword/ad/landing specification while certification is pending, then create it PAUSED when the configuration is validated. Do not wait idle for LegitScript.

---

## 8. Paid + organic landing path

Canonical production URL: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

The production release includes the landing page, sitemap entry, and intentional redirects `/urgent-care-near-you` and `/vip-urgent-care` to the canonical landing. Production Jenkins `main/4` directly smoke-tests the landing and corrected redirect expectations and is SUCCESS.

Landing design: Beverly Hills urgent-care intent, actual phone/address/hours, same-day only `when available`, book + call CTAs, 911/not-emergency-department language, `MedicalClinic` schema, existing first-party attribution via `app.js`, no GA4 injection under current health/privacy allowlist.

`G6-LANDING-PATHS-READY`: GREEN for the first Search pilot, subject to normal live monitoring.

---

## 9. Search Console / GBP / GA4

Search Console property `sc-domain:drfarahvipurgentcare.com`; captured 90-day baseline ~32,325 impressions, 308 clicks, CTR ~0.95%, average position ~11.8. Local query opportunities include urgent-care near-me/Beverly Hills terms around positions 10–16. Continue post-release indexing/canonical monitoring.

GBP location `locations/6719840585856592244`; primary category Urgent care center; captured baseline 5.0 / 109 reviews; regular hours Mon–Thu 08:30–17:30, Fri 08:30–16:30, weekends closed. Open cleanup: inspect Google updates, stale special hours, duplicate/aggressive service catalogue entries.

GA4 production property `489069776`, stream `11211773871`, measurement ID `G-D58FTMF05S`. Selected low-risk public-page architecture remains intentional; sensitive booking/registration/service/treatment/admin surfaces excluded. Open soft validation: Realtime/settings/consent/excluded-page checks. New urgent-care landing remains outside GA4 allowlist; paid attribution uses first-party attribution + completed-visit feedback.

---

## 10. AI / ChatGPT Ads

Active later paid-growth lane. ChatGPT Ads Manager is installed but prior check returned no accessible clinic ad account. Windsor supports an `openai_ads` connector but it is not currently connected. Do not claim eligibility/onboarding yet. Issue #92 remains durable evaluation context. Start account/eligibility/onboarding work after the Google Search pilot's hard launch configuration is complete; do not wait for long-term Google scale learning to begin eligibility work.

---

## 11. Current blockers

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — PARTIAL / SCALE GATE. `validateOnly` HTTP 200 and production promotion complete; first legitimate paid completed-visit import + dedupe + reconciliation still required.
- B-003 Search pilot destination — CLOSED. Production landing/redirect smoke is green and paused RSAs now exist.
- B-004 Google Ads geo positive-location option — UI CHANGED TO PRESENCE; fresh system read-back still required before enable because current connector data is cached.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 exact clinic economics — SOFT; use explicit provisional assumptions.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL until eligibility/onboarding path is completed.
- B-008 Google healthcare certification — WAITING_EXTERNAL / HIGH PRIORITY. Dr. Farah decision + LegitScript application/approval required; then complete Google Ads healthcare certification. Independent safe work continues in parallel.

---

## 12. Exact next actions

1. Keep campaign `24414014329`, all three ad groups and all three RSAs PAUSED until a fresh system read-back confirms Presence-only and final policy/ad review is acceptable.
2. Ask Dr. Farah to complete/approve the LegitScript certification path; when approval is available, use it to complete Google Ads healthcare certification and re-read the affected asset. Do not delete the healthcare service to bypass certification.
3. In parallel, prepare the second `Traveler Care | Beverly Hills | Pre-Arrival` Search campaign: demand/keyword map, overlap negatives, landing requirements, ad copy and measurement plan; create/configure PAUSED only, with no spend until authorized.
4. Prepare replacement clinic/legal-ready Terms of Use and Notice of Privacy Practices requirements for Dr. Farah/legal approval; do not publish invented legal facts.
5. After B-004 fresh read-back and acceptable core ad policy state, proceed with the already-authorized controlled local Search pilot under finite guardrails if no new hard blocker appears.
6. During the pilot, use the first legitimate Google-click completed visit for the controlled Data Manager recording + replay/dedupe + reconciliation acceptance. Keep `Visit Completed` Secondary until passed.
7. Review search terms early, add negatives aggressively, and judge toward completed visits/economics rather than clicks alone.
8. Continue GBP cleanup, Search Console post-release monitoring and GA4 soft validation while certification is pending.
9. Begin ChatGPT Ads eligibility/account-onboarding investigation once final Google launch configuration is complete; any ChatGPT pilot requires finite budget, dedicated source attribution and stop/scale rules.

---

## 13. Resume protocol

Read this file, then `ROADMAP.md`; check `dev`, `main`, exact Jenkins statuses and live Ads state. Preserve the hard spend/privacy/data gates above. Continue safe independent lanes instead of waiting on campaign-data-dependent tests or external certification. Update this handoff after every material session and put durable deferred work/blockers in `ROADMAP.md`.