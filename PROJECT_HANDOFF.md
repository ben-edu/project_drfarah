# PROJECT HANDOFF — Dr. Farah VIP Urgent Care

> **Live unified resume document.** Continue from this file + `ROADMAP.md`; live systems remain authoritative for their own state.

**Last updated:** 2026-11-10  
**Repository:** `ben-edu/project_drfarah`  
**Canonical branch:** `dev`  
**Production branch:** `main`  
**Canonical roadmap:** `ROADMAP.md`

---

## 0E. 2026-11-10 — owner-approved continued Search activity and no-conversion-fee strategy

**OWNER DECISION (this turn):** Preserve current ENABLED state of Urgent Care Search campaign `24414014329` ($10/day **average**) and Traveler Search campaign `24404901753` ($5/day **average**) because Dr. Farah likely re-enabled them. Keep existing Near Me ad group `204328258769` PAUSED for now. The goal is economical real completed visits, not increasing Google-reported conversion counts; do not change ads, Google tags, bids or medical claims without verified necessity, and do not create spending not already authorized.

**FACT — mechanism:** Google Ads Conversion Tracking is a free measurement feature. Under existing Manual CPC / ECPC off, Ads bills ad clicks; Conversion is a report of an action and Cost/conv = paid spend / counted actions, **not a second charge**. `Calls from ads` via call assets does not need a Google Ads website tag on clinical booking pages. Click-to-call is intent, not call answer; a booking request is not confirmed appointment or completed visit. Existing `frontend/analytics.js` sends GA4 limited allowed public pages only, consent-guarded, and intentionally excludes health service/booking/registration; first-party booking attribution is preserved. No Google Tag removal or new Google Ads clinical events is justified by a billing fear alone.

**LIVE CONNECTOR SNAPSHOT — 2026-11-10 (not a guarantee of instantaneous refresh):** Account 652-510-3588 USD/Los Angeles; both Search campaigns ENABLED since 2026-11-09 Google Ads web changes; Near Me paused since Nov 7. Urgent 2026-11-01..10 $302.30 / 73 clicks / 16 reported phone_calls / 8 counted Calls from ads / 37 All Conversions; Beverly Hills $115.22/26 clicks/8 calls, Near Me $160.09/40 clicks/0 counted ad calls (+22 local actions), Walk-In $26.99/7 clicks/0 calls. Travel no sampled spend. Two call assets and six RSA approved in limited reads; all other asset policy coverage incomplete. Average budgets for active campaigns $10 / $5, not hard daily caps; possible ~$456 aggregate monthly budget reference if unchanged and fully active. Separate Local Services system-generated ENABLED and $0 reported sample spend; check independent billing.

**ACTIONABLE GAPS:** (1) native Ads UI: account and per-campaign budgets, keyword CPC bids and modifiers, auto-apply recommendations/automation, Local Services billing; (2) `Calls from ads` minimum duration, Count Every→potential One if actual lead definition supports it, campaign goal selection, Local Actions secondary/diagnostic, approved call reporting/privacy/recording; (3) clinic non-PHI call-to-book-to-visit reconciliation and appropriate future offline completed visits; (4) fix RSA `Urgent Visit From $250` vs site `Starting From $240` once clinic price approved, and verify Walk-In truth; (5) preserve Near Me as a paused experiment, re-evaluate only on real outcomes; (6) check all ad/sitelink/policy approvals and healthcare scope. Avoid unsupported broad certification claims.

**EXECUTION STATUS:** Read-only research and Git documentation ONLY; **no Google Ads platform change, bid/goal mutation, campaign pause, or website tag edit made** in this session. User expressly wants existing live campaigns to remain enabled, but specific changes that affect spend, clinical claims, goals or user tracking must have exact pre/post state and be validated. Native Ads UI/connected API limitations documented. Authoritative detailed runbook `docs/GOOGLE_ADS_COST_CONTROL_CONVERSION_STRATEGY_2026-11-10.md`; integrated priority queue `ROADMAP.md` 3A/3B; issue #110. Next session starts from account readback and clinical price/walk-in/qualified-call truth rather than rebuilding campaigns.

---

## 0D. 2026-11-08 — verified staging medical Hero release + repository governance checkpoint

**OWNER ACCEPTANCE — FACT:** The owner personally tested the new owner-supplied Dr. Farah medical Hero on `staging.drfarahvipurgentcare.com` and accepted its appearance. Remaining image refinements are explicitly lower-priority future Phase D/P3-04 work. The owner reports mobile Call/Book and clinic phone CTAs work; do not revisit their functionality without new evidence.

**SOURCE / RELEASE — FACT:** Owner's original PNG `docs/design/ChatGPT Image Aug 25, 2026, 01_02_02 PM.png` is copied **byte-identically** to `frontend/assets/hero-dr-farah-medical-20260825.png` (Git blob `3ee896f84c04866c40d143930c7298b1e21cbbbb`, 1,854,065 bytes). CSS no longer hides the actual physician Hero/portrait behind weight-loss or pre-op service artwork; mobile/tablet show the full Hero photograph above the headline while preserving existing Call/Book/menu. PR #138 was closed **without merging**, PR #139 exact-head `71b8caaa` succeeded and merged into `dev` as `964471fe65487e5ccf6b800b32f28a0f5f54dc6a` (Jenkins `dev/2` SUCCESS). Exact `PR-140/1` CI SUCCESS; full six-file production PR #140 merged to `main` commit `37794a7490ff338e1648fd788b0c38527fef838a`. Production Jenkins `main/4` status at this checkpoint: **SUCCESS (exact SHA `37794a74`, Jenkins `main/4`)**. Main Jenkins success (if/when confirmed) proves the configured server-side deploy/smoke, not an operator's external phone browser; **the owner has now confirmed the new visual changes are present on the public production site**. Earlier the owner reported Call/Book and phone working. Formal breakpoint-by-breakpoint, apex/www and longer-term cache verification remain unproven; Issue #134 should retain those residual checks (do not claim exhaustive device QA).

**GIT HISTORY — GOVERNANCE:** Before PR #140, earlier emergency hotfix PR #137 had left `main` and `dev` divergent (3 commits on each side). PR #140 was an exact-head, clean full-`dev` visual promotion into `main`, preserving the production Jenkinsfile hotfix and both merge histories. This control-plane documentation commit is built on the new `main` release merge and advanced to `dev` via a lease-checked, **non-force fast-forward** from old dev head `964471fe`. Verified lineage target: `main` is an ancestor of `dev` after the ref update; confirm again with GitHub compare readback. Do not rewrite commits or create a second unnecessary production PR. Document this exception to the normal release-invariant sequence; future work must obey `docs/GIT_RELEASE_STRATEGY.md` and reconcile hotfixes promptly.

**BRANCH CLEANUP — FACT:** 13 branches in initial inventory: 2 permanent (`dev`, `main`), 7 old refs with 0 unique commits and proven ancestors of both permanent branches (safe-prune candidates), and 4 old refs with unique/unmerged commits (retained). Full audited SHA inventory, safe commands and outstanding administrator actions: `docs/repo/BRANCH_AUDIT_2026-11-08.md` and Issue #141. GitHub `delete_branch_on_merge=true`, no open PRs after #140 merge. **Actual remote branch deletion was NOT performed**: connected GitHub toolset offers no delete-ref mutation. Do not report stale refs removed until operator-side deletion has been confirmed. GitHub branch protection endpoint returned HTTP 403, so protection settings were not verified. Jenkins Multibranch branch/PR job duplication and orphaned jobs need an administrator-side SCM-discovery review; do not rerun builds to simulate cleanup.

**SAFETY / DEFERRED:** No Google Ads spend, enablement, patient data, booking backend, PHI, credential or medical offer changes in this visual release and hygiene work. Ads remain PAUSED under the policy/measurement gates in Roadmap. Original roadmap A–N phases and P0–P3 priorities remain intact.

**EXACT RESUME ORDER:** (1) Production Hero was observed by owner and Jenkins `main/4` succeeded. Verify release lineage and any remaining 320/375/680/768/1024px, apex/www/cache QA under Issue #134; no need to reopen the resolved visual-release work. (2) Confirm safe removal of seven merged refs in Issue #141 by an authenticated GitHub admin; retain four divergent branches until archived/reviewed. (3) Resume highest Roadmap P0: Dr. Farah certification/policy reply, Google healthcare certification and call-asset compliance (Issues #106/#110), ad vs site price/walk-in consistency, legal notices and conversion/real completed-visit measurement; keep paid campaigns paused absent explicit authorization. (4) Defer optional picture replacements/optimization and other site polish to Phase D / P3-04.

---

## 0C. 2026-11-08 — roadmap integration and production mobile mismatch

**FACT:** On Nov 8, user personally verified new menu + Call/Book visual UX on staging but reported it **absent from the production site** despite PR #129 merge to `main`. The `main` source repository contains responsive menu JS/CSS. Jenkins exact-head `main/1` SUCCESS and `dev/47` SUCCESS. This does NOT prove that the public production origin is serving those exact bytes. Treat as user-observed P0 incident requiring real HTTP + browser verification, no assumption that previous green CI closed it. Production DNS/HAProxy/Hestia docroot, caching, correct file response, stage skip and Jenkins smoke coverage must be checked. Current Jenkins home smoke only asserts generic "Dr. Farah", not responsive asset markers; cache policy differs between staging (`no-store`) and production (`no-cache`). Suspect cache/stale endpoint is a hypothesis, not proven cause.

**ACTION:** The original roadmap was stale about paused campaign budgets, certification approval path, child status and unfinished mobile code. `ROADMAP.md` section 3A is now the single cross-lane P0–P3 dependency/owner/gate/action queue, preserving all pre-existing A–N phases and BG work IDs. Separately resolve P0-01 deploy discrepancy; do not introduce unauthorized paid traffic.

**RESEARCH (official notice 2026-11-04):** Google announced a future updated US/UK/Canada telemedicine qualification route using NABP Healthcare Merchant Accreditation in addition to LegitScript. Verify effective date, exact clinic eligibility and Google certification before claiming use. NABP official FAQ publicly lists $1,075 first-year application / $1,075 annual thereafter (may have extra domain charges); validate current total and requirements. The 2026-10-31 policy-isolated paid Search / defer LegitScript decision remains in force, and no services should be misrepresented to bypass certification.

**NEXT:** Implement source and production smoke/asset-cache control fix through normal feature -> dev -> main only after user-ready staging acceptance/CI; verify actual production bytes and viewport. Route root-cause records to `docs/` and roadmap P0-01. No Ads enable, conversion edits or new spend in this update.

---

## 0B. 2026-11-08 — independent Google Ads + site forensic audit

**FACT — CI/release:** Jenkins `main/1` and `dev/47` both read SUCCESS on their exact heads `0b7ddb6a31a831d6aa8843c3e42c9b240750a796` and `6931e147fe369b3b8407caa83cc7c174e2ba9e04`. PR #129 production merge and #130 ancestry-only reconciliation are complete. Staging mobile UX received user visual acceptance. Independent real-device production smoke remains a verification task, not a proven failure.

**FACT — Google Ads account** `652-510-3588`, Urgent Care Search pilot `24414014329`: PAUSED, configured $10/day; Traveler Search `24404901753`: PAUSED, $5/day. Historical urgent-care pilot (Nov 2–6) delivered 2,271 impressions, 68 clicks (2.99% CTR), $281.67 cost (~$4.14 CPC), 9 reported phone calls, 3 `Calls from ads` conversions (~$93.89 / platform conversion), 27 All Conversions including 8 directions/15 engagements/1 website visit + 3 calls. Neither reported calls nor conversions demonstrate booked/completed visits. No spend or campaign activation authorized by this audit.

**FACT — key segmentation:** 61/68 clicks and $251.10 (~89% spend) from mobile. Beverly Hills ad group 23 clicks/$101.93/3 ad-call conversions; `Near Me` 40/$160.09/0 ad-call conversions (already PAUSED at ad-group level); Walk-In 5/$19.65/0. Search impression share ~24.95%; rank lost ~26.13%, budget lost ~48.92% — not a reason to scale without verified economics. Manual CPC, enhanced CPC disabled; positive and negative geo presence setting; Search Partners and Display targeted OFF as current configuration, although historical partner impressions without clicks exist.

**FACT — conversion-action audit:** "Calls from ads" is enabled, Primary, type AD_CALL, counting MANY_PER_CLICK. Three Google-hosted Local actions (Directions, Other engagements, Website visits) are also marked Primary for their own goals, but appeared only in All Conversions for the sampled campaign. Primary label alone does not mean campaign bidding uses it; verify its selected account/campaign conversion goals in Google Ads UI. Manual CPC means it is not currently smart-bidding based on these 3 calls. Google auto-tagging true. Connected API currently supports observing but not editing conversion-action goal/count settings.

**FACT — site/code:** Ad headline "Urgent Visit From $250" conflicts with the urgent-care landing page's "Starting From $240" (business source also approx $240). "Walk-In Urgent Care" claim must match actual walk-in acceptance: current online booking is a *request*, pending clinic confirmation. Main/traveler landings use dedicated phone/booking CTAs. Responsive navigation fix merged and staging accepted, but paid media remained 89% mobile before fix. GA4 implementation deliberately *excludes* health-intent paid landings, booking and registration: measured 3 direct GA4 sessions on Oct 15–Nov 7, not a reliable paid-funnel denominator. The code has first-party UTM/GCLID/GBRAID/WBRAID -> booking attribution; live completed-visit import and clinic call/appointment reconciliation remain unproven. `terms.html` and `notice-of-privacy-practices.html` source still state legal-review placeholders; obtain approved text rather than automatically changing it.

**DATA_GAP — priority:** Official connected call dispositions/duration/answer rate and first Google-attributed completed visits; campaign-selected conversion goals and per-action counted lead semantics; approved clinical offers/prices and insurance coverage; search-term negative readback after write (write accepted but cached readback limited); performance of traveler pilot untested (zero actual traffic). Production live browser smoke not independently confirmed from this environment. Historical Google Ads call asset compliance and certification sensitivity remain open.

**RECOMMENDATION — ordered:** (P0) reconcile 9 reported Google calls with answered/qualified/booking/completed outcomes without exposing PHI; correct ad/landing price and walk-in promises; finalize lawful clinic legal notices and call compliance; verify primary vs secondary goals and lead "One" counting; confirm mobile funnel. (P1) preserve PAUSED state until clinic explicit restart; if authorized test tightly controlled local Beverly Hills phrase/exact with $10/day average cap and only qualified services, while Near Me remains PAUSED; set precise stop rules, weekly Search Terms/negatives. (P2) fully validate `visit_completed` offline import/dedup and then evaluate appropriate Smart Bidding; separately pilot traveler/hotel and Pre-Op based on economics and policy; do not open unrestricted PMax/AI Max/remarketing without eligibility/evidence. Daily budget is *average* and can reach ~2x on a given day per Google official policy; review account-level and actual spending if a strict business cap is necessary.

**Detailed evidence and recommendations:** `docs/INDEPENDENT_GOOGLE_ADS_SITE_AUDIT_2026-11-08.md`. This is an analysis and next-action proposal, NOT approval to spend, enable campaigns, change conversions, or modify clinical/legal content. `ROADMAP.md` remains the only master roadmap.

---

## 0A. 2026-11-07 — release reconciliation and independent Google Ads audit checkpoint

**FACT — release:** User approved staging visuals for mobile/tablet navigation and Call/Book actions. PR #129 merged the tested `dev` state into production `main` as commit `0b7ddb6a31a831d6aa8843c3e42c9b240750a796`. PR #130 reconciled the production merge ancestry back to `dev` as `6931e147fe369b3b8407caa83cc7c174e2ba9e04`. GitHub source-branch auto-deletion briefly removed `main` during reconciliation; `main` was immediately restored to its exact prior production merge SHA. Verified `main...dev`: 1 commit ahead, 0 behind and 0 content-file changes. This is correct ancestry, not an outstanding code diff.

**FACT — Jenkins at audit start:** `main/1` and `dev/47` exact-head statuses are still pending; `PR-130/1` successful. Avoid additional branch/CI writes during these builds. Production deployment/smoke are not declared green until verified.

**FACT — Ads at last known live read:** Google Ads account `652-510-3588`; local Urgent Care Search campaign `24414014329` PAUSED at $10/day; Traveler Search `24404901753` PAUSED at $5/day. Prior data: local Search $281.67 / 68 clicks / 3 `Calls from ads` conversions (not patients), reported 9 phone_calls over Nov 1–7. Five targeted competitor/location negatives added. This is not proof of conversion to appointments or completed visits.

**IN PROGRESS — independent account/site audit requested:** Revalidate current Google Ads conversion action settings, ad-call reporting, geo, campaign/search terms, bidding, creatives, assets, search partners, landing experience, privacy/consent, booking source persistence, and policy. Distinguish FACT/HYPOTHESIS/DATA_GAP; document prioritized interventions with verification and retain paused state until explicit operating decision. Any release readback updates and research conclusions must be recorded in canonical handoff on a safe GitHub branch once concurrent Jenkins runs finish.

---

## 0. 2026-11-07 — cost containment, attribution audit and mobile CTA fix

FACT — Google Ads account 652-510-3588: local Search campaign 24414014329 and traveler Search campaign 24404901753 remain PAUSED; 2026-11-07 live readback confirms configured daily budgets were reduced from $40 to $10 and from $20 to $5 respectively. Both budget writes succeeded. No campaign was enabled. Historical 2026-10-28..2026-11-07 local Search spend $281.67 / 68 clicks / 3 reported Conversions. These 3 belong to `Calls from ads` (not verified patients); All Conversions also contains 8 Directions + 15 Other engagements + 1 Website visit. Call connection/duration, appointment, completed visit and realized CAC are not yet reconciled.

FACT — 5 narrowly targeted competitor/location negative keywords were successfully added to local Search: PHRASE "cedars urgent care", "exer urgent care", "excer urgent care", "kaiser urgent care"; EXACT "8767 wilshire blvd urgent care". Do not negative broad legitimate "urgent care near me" without outcome evidence. Search term report revealed $78.34 for 20 clicks on "urgent care near me" and zero primary conversions in the observed period; this is directional, not proof of zero business outcomes.

FACT — PR #126, the documented ads launch strategy/clinic policy decision branch, merged to dev on 2026-11-07 as ebfe2ce5e001ad02d4af62269ffb618f5ef32ce6. Before normal promotion, confirm its Jenkins dev/45 result, lineage main subset dev, and current integrated site state.

IN DEVELOPMENT — dedicated responsive defect issue #127 tracks this change. This responsive-navigation change adds an accessible mobile/tablet menu for widths <=1040px, retains a visible Book CTA in header, labels call CTAs with 310-467-0101, and provides persistent two-button mobile quick actions at <=680px on pages lacking them. Existing pre-op phone-scheduling exception stays phone-first. The change is NOT production-verified merely because code is committed; require branch/staging CI, 320/375/680/768/1024px visual/functional checks, then normal dev -> main release and production smoke.

DECISION/GATE — do not re-enable either paused Search campaign based only on these counts. Clinic-approved call-asset/recording compliance remains a hard gate where applicable; validate real connected calls and completed visits. `Calls from ads` is a reporting conversion (duration/qualification criteria), not an extra charge and not automatically an appointment. The connected write interface does not expose editing conversion-action goals; inspect actual UI settings before changing them.

See `docs/ADS_COST_MOBILE_AUDIT_2026-11-07.md`.

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
