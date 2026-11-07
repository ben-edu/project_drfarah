# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** Continue from this file + `ROADMAP.md`; live systems remain authoritative for their own state.

**Last updated:** 2026-11-07  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 0A. 2026-11-07 — release reconciliation and independent Google Ads audit checkpoint

**FACT — release:** User approved staging visuals for mobile/tablet navigation and Call/Book actions. PR #129 merged the tested `dev` state into production `main` as commit `0b7ddb6a31a831d6aa8843c3e42c9b240750a796`. PR #130 reconciled the production merge ancestry back to `dev` as `6931e147fe369b3b8407caa83cc7c174e2ba9e04`. GitHub source-branch auto-deletion briefly removed `main` during reconciliation; `main` was immediately restored to its exact prior production merge SHA. Verified `main...dev`: 1 commit ahead, 0 behind and 0 content-file changes. This is correct ancestry, not an outstanding code diff.

**FACT — Jenkins at audit start:** `main/1` and `dev/47` exact-head statuses are still pending; `PR-130/1` successful. Avoid additional branch/CI writes during these builds. Production deployment/smoke are not declared green until verified.

**FACT — Ads at last known live read:** Google Ads account `652-510-3588`; local Urgent Care Search campaign `24414014329` PAUSED at $10/day; Traveler Search `24404901753` PAUSED at $5/day. Prior data: local Search $281.67 / 68 clicks / 3 `Calls from ads` conversions (not patients), reported 9 phone_calls over Nov 1–7. Five targeted competitor/location negatives added. This is not proof of conversion to appointments or completed visits.

**IN PROGRESS — independent account/site audit requested:** Revalidate current Google Ads conversion action settings, ad-call reporting, geo, campaign/search terms, bidding, creatives, assets, search partners, landing experience, privacy/consent, booking source persistence, and policy. Distinguish FACT/HYPOTHESIS/DATA_GAP; document prioritized interventions with verification and retain paused state until explicit operating decision. Any release readback updates and research conclusions must be recorded in canonical handoff on a safe GitHub branch once concurrent Jenkins runs finish.

---

## 0. 2026-11-07 — cost containment, attribution audit and mobile CTA fix

FACT — Google Ads account 652-510-3588: local Search campaign 24414014329 and traveler Search campaign 24404901753 remain PAUSED; 2026-11-07 live readback confirms configured daily budgets were reduced from $40 to $10 and from $20 to $5 respectively. Both budget writes succeeded. No campaign was enabled. Historical 2026-10-28..2026-11-07 local Search spend $281.67 / 68 clicks / 3 reported Conversions. These 3 belong to \`Calls from ads\` (not verified patients); All Conversions also contains 8 Directions + 15 Other engagements + 1 Website visit. Call connection/duration, appointment, completed visit and realized CAC are not yet reconciled.

FACT — 5 narrowly targeted competitor/location negative keywords were successfully added to local Search: PHRASE "cedars urgent care", "exer urgent care", "excer urgent care", "kaiser urgent care"; EXACT "8767 wilshire blvd urgent care". Do not negative broad legitimate "urgent care near me" without outcome evidence. Search term report revealed $78.34 for 20 clicks on "urgent care near me" and zero primary conversions in the observed period; this is directional, not proof of zero business outcomes.

FACT — PR #126, the documented ads launch strategy/clinic policy decision branch, merged to dev on 2026-11-07 as ebfe2ce5e001ad02d4af62269ffb618f5ef32ce6. Before normal promotion, confirm its Jenkins dev/45 result, lineage main subset dev, and current integrated site state.

IN DEVELOPMENT — dedicated responsive defect issue #127 tracks this change. This responsive-navigation change adds an accessible mobile/tablet menu for widths <=1040px, retains a visible Book CTA in header, labels call CTAs with 310-467-0101, and provides persistent two-button mobile quick actions at <=680px on pages lacking them. Existing pre-op phone-scheduling exception stays phone-first. The change is NOT production-verified merely because code is committed; require branch/staging CI, 320/375/680/768/1024px visual/functional checks, then normal dev -> main release and production smoke.

DECISION/GATE — do not re-enable either paused Search campaign based only on these counts. Clinic-approved call-asset/recording compliance remains a hard gate where applicable; validate real connected calls and completed visits. \`Calls from ads\` is a reporting conversion (duration/qualification criteria), not an extra charge and not automatically an appointment. The connected write interface does not expose editing conversion-action goals; inspect actual UI settings before changing them.

See \`docs/ADS_COST_MOBILE_AUDIT_2026-11-07.md\`.

---

## 1. Operating model

Growth Acceleration / parallel execution. Independent safe lanes continue while external dependencies wait. Hard-gate only production breakage, privacy/security, data integrity, policy prohibition or unauthorized spend. Real-data tests that inherently require traffic belong inside controlled pilots. Optimize toward completed visits and defensible economics.

Never send unnecessary patient PII/PHI, reason-for-visit or clinical content to marketing systems.

User-facing project explanations default to Persian script; use exact English UI labels only when useful.

Git/release control follows `docs/GIT_RELEASE_STRATEGY.md`: normal flow is `feature/fix/docs -> dev -> main`; current `main` must be contained in `dev` before normal promotion; production-only exceptions must be reconciled back into `dev`. Avoid redundant Jenkins builds.

---

## 2. Current Git / deployment state

FACT — before this final visual/docs release batch, `dev` head `a082d584ea09904363a38d38ec59b368bd4305b8` passed Jenkins `dev/43`.

FACT — PR #123 merged the exact green head `62c71c6a91796f0b9f2cb3fc05348bde8482d650` into `dev`. This brought the real uploaded service-image mapping and responsive hero changes into the integration branch.

FACT — the user visually reviewed staging after the service-image refresh and confirmed that the new images are materially better. Website development is intentionally paused for now so the project can return to Google Ads, but the website is NOT considered finished.

KNOWN WEBSITE DEFECT — mobile/tablet navigation/menu visibility/usability remains poor and requires a dedicated later responsive-navigation implementation. This is durably tracked in `ROADMAP.md` / issue #114 and must not be forgotten.

RELEASE HYGIENE — legacy/fake test assets and duplicate upload-name files are removed in the final release-cleanup batch before production promotion. The active service-image mapping must use only the accepted service assets.

DECISION — after the final release-cleanup/docs SHA is CI-green, promote it through the normal `dev -> main` path. Live `main` is authoritative for the exact production SHA after merge.

---

## 3. Booking / first-party attribution / completed outcome

`G1 BOOKING HEALTHY`: GREEN unless a new regression appears.

Production supports source/UTM, GCLID/GBRAID/WBRAID, opaque marketing session ID, first/last-touch context and partner/traveler markers. `appointment_attributions` is 1:1 and persisted atomically with booking. Marketing attribution excludes page path, service, reason-for-visit, patient PII and clinical content.

`visit_completed`: authoritative appointment status `completed`; deterministic transaction key `visit_completed:<appointment_id>`; occurrence time `starts_at`; non-clinical attribution only.

Google Data Manager validate-only acceptance is complete: a real request returned HTTP 200. First legitimate completed paid visit remains the live recording + replay/dedupe + reconciliation acceptance. Keep `Visit Completed` Secondary until that passes.

---

## 4. Local Google Search pilot

Google Ads customer `652-510-3588`.

Campaign `24414014329` — `Search | Urgent Care | Beverly Hills | Pilot | 2026-10-28` — PAUSED.

- Manual CPC; provisional configured $40/day; no authorized spend.
- Five-mile Beverly Hills targeting and clinic-hours schedule.
- Exact/Phrase positives + negatives; no Broad.
- Three PAUSED ad groups and three PAUSED RSAs.
- Live campaign read confirms positive geo `PRESENCE`.
- Production landing: `https://drfarahvipurgentcare.com/urgent-care-beverly-hills`.

Ad groups:
1. `Urgent Care | Beverly Hills` — `196894367450` — $4.50 default CPC.
2. `Urgent Care | Near Me` — `204328258769` — $4.50 default CPC.
3. `Walk-In | Same-Day` — `199388744537` — $4.00 default CPC.

RSAs: `829832740743`, `829881874987`, `829963008380`.

Keyword Planner: `urgent care beverly hills` ~1,000 average monthly searches, MEDIUM competition, historical average CPC ~$3.56. Do not change bids from planner data alone.

NEXT — after the current release/docs closure, return to Google Ads: review Dr. Farah's response, policy/certification implications, ad/asset status and controlled-launch readiness. Do not enable/spend without explicit authorization.

---

## 5. Traveler / pre-arrival Google Search pilot

Campaign `24404901753` — `Search | Traveler Care | Beverly Hills | Pre-Arrival | Pilot | 2026-10-29` — PAUSED.

- Manual CPC; configured $20/day while paused; no authorized spend.
- US geography, English, 06:00–22:00 schedule.
- EU political-ad declaration: No.
- Live campaign read confirms `PRESENCE`.
- 36 Exact/Phrase positives + 32 campaign negatives.
- Policy-safe assets: four callouts, one structured snippet, four sitelinks.
- Dedicated landing: `https://drfarahvipurgentcare.com/traveler-medical-care-beverly-hills`.

Ad groups:
1. `Traveler Doctor | Beverly Hills` — `200882856919` — $3.50 default CPC.
2. `Hotel Medical Care | Beverly Hills` — `203251601244` — $3.50 default CPC.
3. `Visitor Urgent Care | Beverly Hills` — `200882859839` — $4.00 default CPC.

RSAs: `829861283229`, `829861321812`, `829991120837`.

Keyword evidence supports a precise initial pilot. Do not broaden blindly into expensive generic Beverly Hills doctor/concierge traffic.

DATA_GAP — current connector can return zero ad/asset-level policy rows even when campaign-level reads work. Zero rows are not approval.

---

## 6. Google healthcare policy / LegitScript

FACT — `Clinic Services` sitelink asset `434419668405` pointing to `/services` is DISAPPROVED for `PRESCRIPTION_DRUG_SALE` with missing United States certification and limited under `HEALTH_IN_PERSONALIZED_ADS`.

DECISION — do not delete/hide the legitimate service to bypass policy.

Correct path: Dr. Farah completes LegitScript Healthcare Merchant Certification for `drfarahvipurgentcare.com`; after approval, complete Google healthcare certification for child account `652-510-3588`, US telemedicine/prescription-drug services. Issue #106 tracks this.

NEW FACT — Dr. Farah has now responded. Her response has not yet been interpreted in this handoff; review it as the immediate next Google Ads/certification task. Do not assume from the existence of a response that LegitScript or Google certification is approved.

Do not request portal passwords, payment details, PHI or patient records.

Last verified standard LegitScript pricing (2026-10-29): $975 non-refundable application fee + $2,150 annual certification after approval; standard first-year total $3,125.

SITE READINESS GAP — clinic/legal-approved Terms and Notice of Privacy Practices are still required before final certification readiness.

Certification does not remove Google's separate health-sensitive personalization restrictions.

---

## 7. Call asset / mandatory post-certification review

Issue #110 is OPEN.

The Google Ads call asset for `310-467-0101` was rejected because the account has not completed the applicable Call Ads Supplemental Terms/compliance path.

Do not blindly accept call-recording terms for a healthcare advertiser. Clinic/legal must determine the applicable HIPAA Covered Entity / Business Associate implications. If required, request Google Support exclusion from monitoring/recording before retrying the call asset. Call recording remains off unless clinic/legal explicitly approves.

Issue #110 also mandates a full post-certification review of both campaigns, all ads/assets, policies and landing destinations. Do not close it early.

---

## 8. Search / website growth state

Search Console property: `sc-domain:drfarahvipurgentcare.com`.

High-priority evidence remains concentrated around urgent-care near-page-one queries and strong-ranking Pre-Op medical-clearance queries with low CTR. The first evidence-led urgent-care + Pre-Op title/meta/on-page improvement batch is production-deployed.

Production indexing architecture is intentional: source/staging pages may contain `noindex`; production preparation removes it and installs production robots/sitemap behavior. Do not remove staging noindex as an SEO fix.

### 2026-10-31 visual/image work completed
- real uploaded service images mapped to service pages;
- PRP and Weight Loss use different images;
- Urgent Care, IV, Pre-Op, Virtual, Hotel/Traveler and Traveler Medical use distinct service assets;
- mobile/tablet hero presentation improved so imagery is separated from overlaid text;
- user reviewed staging and accepted the new image quality as materially improved;
- legacy/fake test assets are not to remain in the final production release tree.

### Website development still open
The site is not considered fully finished. The most explicit current defect is mobile/tablet navigation: the menu bar/navigation is not adequately visible/usable. A dedicated responsive navigation pass is required later, along with continuing visual hierarchy/spacing/typography/accessibility/performance QA. This work is recorded in `ROADMAP.md` / issue #114 and is deferred only so the project can return to Google Ads now.

---

## 9. GBP / GA4 / AI Ads

GBP location `locations/6719840585856592244`; primary category `Urgent care center`; captured baseline 5.0 / 109 reviews. Core factual cleanup/reputation cadence remains open.

GA4 property `489069776`, stream `11211773871`, measurement `G-D58FTMF05S`. Safe public-page allowlist remains intentional; sensitive health-intent landings remain outside the current GA4 allowlist. Soft receipt/settings validation remains.

ChatGPT Ads remains a later paid-growth lane. Ads Manager installed; prior discovery found no accessible clinic ad account; Windsor `openai_ads` has no connected account. No spend without policy/measurement/budget gates.

---

## 10. Current blockers / gates

- B-001 Booking/Brevo — CLOSED.
- B-002 Data Manager — SCALE GATE only: first legitimate live completed-visit import + replay/dedupe + reconciliation.
- B-003 Local paid destination — CLOSED.
- B-004 Local campaign geo — CLOSED; live readback `PRESENCE`.
- B-005 GA4 live receipt/settings — SOFT.
- B-006 authoritative clinic economics/capacity — SOFT.
- B-007 ChatGPT Ads eligibility/account access — SOFT / WAITING_EXTERNAL.
- B-008 LegitScript + Google healthcare certification — ACTIVE EXTERNAL / HIGH PRIORITY; issue #106; Dr. Farah response received and pending review.
- B-009 Traveler landing production readiness — CLOSED.
- B-010 Call asset compliance/post-cert review — OPEN; issue #110.
- B-011 Git release alignment — enforce `main ⊆ dev`; current visual release is moving through normal `dev -> main` promotion.
- B-012 Website visual/responsive development — PARTIAL / OPEN; issue #114. Image refresh accepted; mobile/tablet navigation remains defective and further site polish is planned.
- B-013 Ad/asset policy readback — DATA_GAP; do not infer approval from zero rows.

---

## 11. Exact next actions

1. Finish the final site visual/docs release: remove fake/duplicate image artifacts, CI-validate exact SHA, merge to `dev`, then promote validated `dev` to `main` and production.
2. Immediately after release closure, review Dr. Farah's new response and determine exact LegitScript / Google healthcare certification / call-asset actions.
3. Re-read all six RSA and relevant asset policy/review statuses when a fresh source is available.
4. Keep both Search campaigns PAUSED until policy/readiness review and explicit spend authorization are satisfied.
5. Resolve issue #110 call-asset compliance path and preserve mandatory post-certification full review.
6. Later website pass: implement mobile/tablet navigation and continue responsive/accessibility/performance/visual polish; do not treat the current site as development-complete.
7. Continue GBP factual cleanup, Search Console monitoring and GA4 soft validation in parallel where useful.
8. First legitimate paid completed visit → Data Manager live import + replay/dedupe + reconciliation; keep `Visit Completed` Secondary until passed.
9. ChatGPT Ads remains later, after final Google launch configuration is stable.

---

## 12. Resume protocol

Read this file, then `ROADMAP.md`; check exact `dev`, `main`, Jenkins statuses, branch lineage and live Ads state. Before any Git write that can trigger CI, verify no relevant build is already pending/running. Before production promotion, enforce `docs/GIT_RELEASE_STRATEGY.md`. Preserve spend/privacy/data/policy hard gates. Continue safe independent lanes instead of waiting on external dependencies. Never recreate existing campaign/ad objects without live read-back. Update this handoff after material sessions and keep deferred work in `ROADMAP.md`/issues.
