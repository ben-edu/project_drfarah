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

FACT — `dev/28` SUCCESS on `d31807e929f725e6ab35b432c8cdbed03bc52047`.

FACT — PR #108 (`Prioritize traveler campaign and healthcare certification lane`) passed Jenkins PR-head CI and was merged to `dev`; resulting merge SHA `46ebf6fb697cb270cce99bef1723c0879860d1e1`. Jenkins `dev/29` is pending at this handoff update.

FACT — production `main` remains `5e34eea5ca5c1b78a0aeceb2a4fa287b7b15e1ae`; Jenkins `main/4` SUCCESS. Production includes the urgent-care Beverly Hills landing path and Data Manager runtime work.

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

DATA_GAP — Windsor currently returns cached pre-change `PRESENCE_OR_INTEREST` and the connected plan cannot force-refresh. Require fresh system read-back before enable. Do not interpret the stale connector value as proof the UI save failed.

DECISION — keep the local urgent-care campaign Presence-only. Pre-arrival traveler demand is handled separately.

---

## 5. Traveler / pre-arrival Google Search campaign

FACT — second Search campaign created in Google Ads on 2026-10-29:

- Campaign ID: `24404901753`
- Name: `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29`
- Status: PAUSED
- Bidding: Manual CPC
- Configured daily budget: $20/day; this is configuration only while PAUSED and is **not authorization to launch/spend**
- EU political ads declaration: No
- Geography: United States geo target configured
- Language: English
- Schedule: 06:00–22:00 daily in the Google Ads account time zone

PAUSED ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — default CPC $3.50.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — default CPC $3.50.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — default CPC $4.00.

FACT — 36 positive keywords created PAUSED, using Exact/Phrase only across the three intent groups.

FACT — 32 campaign-level negatives added to control waste/cannibalization and keep certification-sensitive intent out of this campaign for now. Negatives include `near me` to route immediate local intent toward the local campaign, plus emergency/hospital, jobs/training, dental/vet, free/cheap, prescription/refill/pharmacy/medication, telehealth/telemedicine/virtual/online doctor, and unrelated treatment terms.

DECISION — do not point this campaign at the existing `/hotel-traveler-care` page for the paid pilot because that page contains virtual-care/prescription-refill language that can trigger the same Google healthcare certification policy. Build a dedicated in-person/pre-arrival traveler landing page without prescription/telemedicine claims.

IN PROGRESS — branch `growth/traveler-prearrival-landing-20261029` creates `frontend/traveler-medical-care-beverly-hills.html` and adds it to the sitemap. Intended production URL: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

Landing policy boundary: clinic + approved hotel/mobile visit messaging only; no telemedicine prescribing/refill claims; same-day only `when available`; 911/not-emergency-care language; booking + call CTA; first-party `app.js`; no intentional GA4 injection on this health-intent landing.

NEXT for traveler campaign after the new landing is green in production: create PAUSED RSAs + safe campaign assets pointing only to the new landing/other policy-safe URLs; perform geo/policy read-back; keep the campaign PAUSED until a separate launch/budget authorization and all launch gates pass.

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

Production urgent-care landing: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`; `main/4` production smoke GREEN.

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
- B-009 Traveler landing production readiness — ACTIVE. New policy-safe landing must pass CI and production promotion before traveler RSAs are created against it.

---

## 10. Exact next actions

1. Require Jenkins `dev/29` green for PR #108 merge SHA; diagnose if it fails.
2. Finish branch `growth/traveler-prearrival-landing-20261029`: policy-safe traveler landing + sitemap + this handoff; open PR to `dev`, require exact-head CI green, merge.
3. Promote validated traveler landing to `main` when normal production gates permit; require production CI/smoke evidence before using it as an ad destination.
4. Then create traveler campaign RSAs and policy-safe assets PAUSED against the new production landing; do not enable campaign or incur spend yet.
5. Obtain fresh Google Ads read-back for local campaign Presence-only; final policy/readiness review before any local pilot enable.
6. Dr. Farah continues LegitScript external lane. After approval, complete Google healthcare certification and re-read affected assets.
7. Continue GBP, Search Console and GA4 soft lanes in parallel.
8. First legitimate paid completed visit → Data Manager live import + replay/dedupe + reconciliation; keep `Visit Completed` Secondary until passed.
9. Start ChatGPT Ads eligibility/account work after final Google launch configuration is stable.

---

## 11. Resume protocol

Read this file, then `ROADMAP.md`; check `dev`, `main`, exact Jenkins statuses and live Ads state. Preserve hard spend/privacy/data gates. Continue safe independent lanes instead of waiting on external certification or campaign-data-dependent tests. Never recreate existing campaign/ad objects without live read-back. Update this handoff after every material session and put durable deferred work/blockers in `ROADMAP.md`.
