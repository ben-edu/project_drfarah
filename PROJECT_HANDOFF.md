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

Git/release control follows `docs/GIT_RELEASE_STRATEGY.md`: normal flow is `feature/fix/docs -> dev -> main`; current `main` must be contained in `dev` before normal production promotion; any production-only hotfix/selective release must be immediately reconciled back into `dev`.

---

## 2. Branch / deployment state

FACT — PR #109 (`Add traveler pre-arrival landing for second Search campaign`) passed exact-head CI and merged to `dev`; current pre-reconciliation `dev` SHA is `04c97249e6c793824f3659cbdf5170c425682356`.

FACT — Jenkins `dev/30` SUCCESS on `04c97249e6c793824f3659cbdf5170c425682356`.

FACT — PR #111 (`Promote traveler medical-care landing to production`) passed exact-head CI on `f67ca1b0045c6fc10459765e6da29cfda289f019` and merged to `main`; current `main` SHA is `9cb6b0def117a9f1863a37216fd8460b47a220be`.

FACT — PR #111 was a narrow production promotion because `dev` and `main` had accumulated divergent history after production-only recovery work. The user approved correcting that process permanently.

DECISION — normal releases are now `dev -> main`. Before such a release, `dev` must contain current `main`. A direct production hotfix/selective release is exceptional and is not complete until `main` has been reconciled/back-merged into `dev` and the reconciled `dev` state passes CI.

IN PROGRESS — controlled reconciliation branch `chore/git-release-strategy-reconcile-20261029` will create a two-parent merge of current `dev` + current `main`, preserve validated `dev` content, import the production Jenkins redirect-smoke correction, and add the approved Git strategy documentation. Direct raw PR #112 (`main -> dev`) is superseded by this controlled reconciliation because its merge-base diff is misleading for files already present on both heads.

DATA_GAP — after PR #111 merge, production `main` Jenkins result for `9cb6b0d...` had not yet posted a distinct `main` branch status at this handoff update. Do not infer production success from the PR-head success alone; verify the actual `main` build/smoke result.

---

## 3. Booking / attribution / completed outcome

`G1-BOOKING-HEALTHY`: GREEN unless a new regression appears.

Production supports source/UTM, GCLID/GBRAID/WBRAID, opaque marketing session ID, first/last-touch context and partner/traveler markers. `appointment_attributions` is 1:1 and persisted atomically with booking. Marketing attribution excludes page path, service, reason-for-visit, patient PII and clinical content.

`visit_completed`: authoritative appointment status `completed`; deterministic transaction key `visit_completed:<appointment_id>`; occurrence time `starts_at`; non-clinical attribution only.

Google Data Manager validate-only acceptance is complete: real request returned HTTP 200. First real eligible paid completed visit remains the live recording + replay/dedupe + reconciliation acceptance. Keep `Visit Completed` Secondary until that passes.

---

## 4. Local Google Search pilot

Google Ads customer `652-510-3588`.

Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28` — PAUSED. Manual CPC, provisional $40/day, five-mile Beverly Hills proximity, clinic-hours schedule, Exact/Phrase positives and negatives. Three PAUSED ad groups and three PAUSED RSAs exist against `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

FACT — on 2026-10-29 the user changed the positive location option in the Google Ads UI to Presence-only (`people in or regularly in the targeted locations`).

DATA_GAP — Windsor previously returned cached pre-change `PRESENCE_OR_INTEREST`; require fresh system read-back before enable. Do not interpret stale connector data as proof the UI save failed.

DECISION — keep the local urgent-care campaign Presence-only. Pre-arrival traveler demand is handled separately.

---

## 5. Traveler / pre-arrival Google Search campaign

FACT — second Search campaign created in Google Ads on 2026-10-29:

- Campaign ID: `24404901753`
- Name: `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`
- Status: PAUSED
- Bidding: Manual CPC
- Configured daily budget: $20/day; configuration only while PAUSED and **not authorization to launch/spend**
- EU political ads declaration: No
- Geography: United States
- Language: English
- Schedule: 06:00–22:00 daily in the Google Ads account time zone

PAUSED ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — default CPC $3.50.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — default CPC $3.50.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — default CPC $4.00.

FACT — 36 positive keywords created PAUSED, Exact/Phrase only.

FACT — 32 campaign-level negatives added for waste/cannibalization/policy control, including local `near me`, emergency/hospital, jobs/training, dental/vet, free/cheap, prescription/refill/pharmacy/medication, telehealth/telemedicine/virtual/online doctor, and unrelated treatment terms.

FACT — user changed traveler campaign `24404901753` positive location option in the Google Ads UI to Presence-only.

FACT — policy-safe campaign assets created while PAUSED: four callouts, one structured snippet and four sitelinks. Attempted call asset for `310-467-0101` was rejected because the account has not completed the Call Ads Supplemental Terms/compliance flow.

BLOCKER/FOLLOW-UP — issue #110 tracks healthcare/HIPAA-safe call-asset resolution and a mandatory post-certification review of all ads/assets/policies across both Search campaigns. Do not silently skip this after LegitScript/Google healthcare certification.

DECISION — do not point this campaign at the existing `/hotel-traveler-care` page for the paid pilot because that page contains virtual-care/prescription-refill language. Dedicated policy-safe production landing is `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

FACT — traveler landing is integrated on `dev`, PR #109 CI is green, and the narrow production promotion PR #111 merged to `main`. Actual production `main` build/smoke still requires read-back before the URL is treated as production-validated.

NEXT for traveler campaign after production landing is confirmed green: create three PAUSED RSAs against the production traveler landing, read back geo/policy/serving status, and keep the campaign PAUSED until separate launch/spend authorization and all launch gates pass.

---

## 6. Google healthcare policy / LegitScript

FACT — sitelink `Clinic Services` pointing to `/services` is DISAPPROVED for `PRESCRIPTION_DRUG_SALE` with missing certification for the United States and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete/hide the legitimate service to bypass policy. Correct path: Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`; after approval, complete Google Ads healthcare certification for child account `652-510-3588`, United States, telemedicine/prescription-drug services. Issue #106 tracks this.

WAITING_EXTERNAL — Dr. Farah decision/application/payment/approval. Do not request portal passwords, payment details, PHI or patient records.

FACT — standard LegitScript pricing verified 2026-10-29: $975 non-refundable application fee + $2,150 annual certification after approval; standard first-year total $3,125.

SITE READINESS GAP — `frontend/terms.html` is still draft/pending legal review and `frontend/notice-of-privacy-practices.html` is still a placeholder. Clinic/legal-approved content is required before final certification readiness.

Certification does not remove Google's separate health-sensitive personalization restrictions. Do not use prohibited health remarketing/Customer Match workarounds.

---

## 7. Landing / SEO / local / analytics

Production urgent-care landing: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`; prior production `main/4` smoke GREEN.

Traveler landing intended/current production path after PR #111: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`; require new `main` build/smoke evidence before declaring production validation complete.

Search Console property: `sc-domain:drfarahvipurgentcare.com`. Traveler/tourist/hotel query filter returned no rows in the recent connected Search Console pull; treat traveler demand as a paid hypothesis to test, not proven organic volume.

GBP location `locations/6719840585856592244`; primary category Urgent care center; baseline 5.0 / 109 reviews. GBP cleanup/reputation cadence remains open.

GA4 property `489069776`, measurement ID `G-D58FTMF05S`; selected low-risk public-page allowlist remains intentional. Sensitive health-intent landings stay outside the current GA4 allowlist; first-party attribution + completed-visit feedback are the paid measurement backbone.

---

## 8. AI / ChatGPT Ads

Later paid-growth lane. ChatGPT Ads Manager is installed but prior account discovery found no accessible clinic ad account. Windsor exposes `openai_ads` but no account is connected. Begin eligibility/onboarding after final Google launch configuration is stable; do not wait for long-term Google optimization learning where work is independent.

---

## 9. Current blockers / gates

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — SCALE GATE only: first legitimate live completed-visit import + replay/dedupe + reconciliation.
- B-003 Local Search destination — CLOSED.
- B-004 Local campaign geo — UI CHANGED TO PRESENCE; fresh system read-back required before enable.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 exact clinic economics — SOFT.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL.
- B-008 LegitScript + Google healthcare certification — WAITING_EXTERNAL / HIGH PRIORITY; independent work continues.
- B-009 Traveler landing production readiness — PR #111 MERGED; actual `main` production CI/smoke read-back still required.
- B-010 Call asset compliance — OPEN / issue #110. Resolve through Google healthcare/HIPAA-safe Communication Features path; do not blindly accept call-recording terms.
- B-011 Git branch reconciliation — ACTIVE. Complete controlled current `main -> dev` reconciliation and validate reconciled `dev`; after closure, enforce `main`-contained-in-`dev` invariant before normal releases.

---

## 10. Exact next actions

1. Complete controlled Git reconciliation branch `chore/git-release-strategy-reconcile-20261029`: preserve validated `dev`, import production Jenkins redirect-smoke fix/history, add `docs/GIT_RELEASE_STRATEGY.md`, update decisions/operating model, and create a two-parent merge with current `main`.
2. Require exact-head CI green on the reconciliation PR; merge to `dev`; verify branch lineage shows current `main` contained in `dev`; close/supersede raw PR #112.
3. Verify actual production Jenkins `main` build/smoke for `9cb6b0def117a9f1863a37216fd8460b47a220be`; do not substitute PR #111 success for production success.
4. Once traveler landing is production-green, create three traveler campaign RSAs PAUSED against the new landing; read back geo/policy/serving state.
5. Obtain fresh Google Ads read-back for both campaigns' Presence-only setting and final core policy/readiness status.
6. Dr. Farah continues LegitScript external lane. After approval, complete Google healthcare certification and execute issue #110 post-certification review/call-asset resolution.
7. Continue GBP, Search Console and GA4 soft lanes in parallel.
8. First legitimate paid completed visit → Data Manager live import + replay/dedupe + reconciliation; keep `Visit Completed` Secondary until passed.
9. Start ChatGPT Ads eligibility/account work after final Google launch configuration is stable.

---

## 11. Resume protocol

Read this file, then `ROADMAP.md`; check `dev`, `main`, exact Jenkins statuses, branch lineage and live Ads state. Before any production promotion, enforce `docs/GIT_RELEASE_STRATEGY.md`: if current `main` is not contained in `dev`, reconcile first. Preserve hard spend/privacy/data gates. Continue safe independent lanes instead of waiting on external certification or campaign-data-dependent tests. Never recreate existing campaign/ad objects without live read-back. Update this handoff after every material session and put durable deferred work/blockers in `ROADMAP.md`.
