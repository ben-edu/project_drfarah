# Independent Google Ads + Website Growth Audit — 2026-11-07

**Project:** Dr. Farah VIP Urgent Care  
**Evidence date:** 2026-11-07 (Google Ads observation mostly 2026-11-02 through 2026-11-06)  
**Scope:** Google Ads customer \`652-510-3588\`, GA4 \`489069776\`, Search Console \`sc-domain:drfarahvipurgentcare.com\`, GBP \`locations/6719840585856592244\`, GitHub \`ben-edu/project_drfarah\` on \`dev\`.  
**Authority:** current connector values for live account state; GitHub code for implemented design; clinic operations for confirmed patient outcomes. Site HTTP/page-speed production fetch could not be completed through available remote retrieval, so runtime page speed/production visual verification is **not claimed**.  
**Status:** review/recommendations, not authorization to enable campaigns or spend.

## 1. Release / source-of-truth checkpoint

- \`main\` = \`0b7ddb6a31a831d6aa8843c3e42c9b240750a796\` (PR #129 production promotion of the staging-reviewed responsive mobile CTA fix).
- \`dev\` = \`6931e147fe369b3b8407caa83cc7c174e2ba9e04\` (PR #130 main-to-dev ancestry reconciliation).
- \`main...dev\` has zero changed files; one reconciliation history commit. Main was temporarily removed by PR auto-deletion, but restored to the same original production SHA.
- Jenkins at start of this audit: \`main/1\` and \`dev/47\` **PENDING**; PR #130/1 successful. Do not claim production build green.
- Responsive menu, mobile Call 310-467-0101 and Book actions were tested and staging visually accepted by user. Full post-production smoke remains pending.

## 2. Observed live Google Ads performance (Urgent Care pilot)

\`24414014329\` PAUSED; configured budget reduced $40 to **$10/day** (live readback); Manual CPC, enhanced CPC OFF. Traveler pilot \`24404901753\` PAUSED and reduced $20 to **$5/day**. Legacy Smart paused; system-generated Local Services enabled but 0 spend/impressions in observed Ads window (separate inventory/eligibility still needs check).

Local campaign 2026-11-02 to 2026-11-06:
- 2,271 impressions / 68 clicks / 2.99% CTR / $4.1422 avg CPC / $281.67 spend.
- 9 reported phone_calls; 3 primary Conversions, all \`Calls from ads\`; 27 \`All conversions\`: 3 ad calls + 8 directions + 15 other local engagements + 1 website visit. No confirmed patients, no validated CAC.
- Average reported cost per platform conversion: $93.89; per reported phone_call: $31.30 (NOT cost per qualified patient).
- 61/68 clicks MOBILE (89.7%), 6 desktop, 1 tablet; mobile cost $251.10 (89.1%).
- Search impression share 24.95%, lost impression share to budget 48.92% and rank 26.13% in the observed budget regime; do not treat lost share as a reason to raise budgets before ROI proof.
- Ad group: \`Urgent Care | Beverly Hills\` 23 clicks/$101.93/3 Calls-from-ads conversions (reported CPA $33.98); \`Urgent Care | Near Me\` 40/$160.09/0, presently PAUSED; \`Walk-In | Same-Day\` 5/$19.65/0. Conversion sample small and BH group's 3 calls include one on competitor-branded \`cedars urgent care wilshire\`.
- Search terms visible represent only 53 of 68 clicks and ~$216.52 of $281.67 spend (Search Terms report is incomplete due reporting/privacy thresholds); do not imply full intent coverage.
- Specific terms: \`urgent care near me\` 20/$78.34/0 platform conversions; \`urgent care\` 5/$21.50/0; \`cedars urgent care wilshire\` 6/$26.80/1; \`urgent care pico robertson\` 2/$8.98/1; \`urgent care on robertson\` 1/$4.49/1. The last two local references may have competitor/location intent: do not equate with a completed patient.
- Five new local campaign negatives added successfully 2026-11-07: PHRASE \`cedars urgent care\`, \`exer urgent care\`, \`excer urgent care\`, \`kaiser urgent care\`, and EXACT \`8767 wilshire blvd urgent care\`. A cached read did not yet show these fresh writes; Google Ads action reported success; validate in live UI / fresh read before claiming permanent suppression. Google negatives do not match close variants automatically.

## 3. Campaign configuration and quality diagnostics

- Local pilot has 5-mile Beverly Hills proximity, positive geo \`PRESENCE\`; Mon–Thu 08:30–17:30, Fri 08:30–16:30 (account timezone should be verified). Both Google Search and Search Network reporting observed; Search Partners had 131 impressions/0 clicks/$0, and current network target flags Search Partners OFF, Display OFF. Do not attribute spend to partners.
- Exact/Phrase keyword targeting, not unrestricted broad; currently the Near-Me ad group is PAUSED and the other two ad groups ENABLED inside PAUSED campaign.
- Keyword diagnostic: \`urgent care beverly hills\` and \`beverly hills urgent care\` quality score **10/10**, ABOVE_AVERAGE ad relevance and AVERAGE landing-page experience; \`urgent care near me\`, \`nearest urgent care\` **6/10**, ABOVE_AVERAGE ad relevance and BELOW_AVERAGE landing-page experience; \`walk in clinic near me\` **6/10**, BELOW_AVERAGE ad relevance. Quality Score is diagnostic, not a bidding KPI.
- Local RSAs approved at ad-level in earlier detailed readback; strengths AVERAGE/AVERAGE/POOR for local groups, but campaign PAUSED makes primary delivery NOT_ELIGIBLE (not proof of policy rejection). Traveler RSAs show GOOD/GOOD/AVERAGE strengths; no traveler spend in observed period.
- **Definite ad-site mismatch:** local RSA headlines say \`Urgent Visit From $250\` while urgent-care landing / price display says \`Starting From $240\`; clinic should verify authoritative price first, then synchronize all Google Ads assets and page. Also \`Walk-In Urgent Care\` headline must not promise unconfirmed walk-in availability if the site uses appointment requests.
- Manual CPC + Enhanced CPC OFF means Google was not using Smart Bidding to optimize this pilot toward those conversion actions. Existing conversion labels are measurement/goals hygiene concerns, not proof Google wasted spend chasing conversions.

## 4. Measurement and caller attribution — key gaps

- Account auto-tagging ENABLED and call reporting / call-conversion reporting ENABLED; account call conversion points to \`conversionActions/179\`. \`Calls from ads\` conversion counts MANY_PER_CLICK, primary for goal; \`Visit Completed\` exists but SECONDARY and ONE_PER_CLICK; the 30-day attribution window applies to those actions. \`Local actions - Directions\`, \`Other engagements\`, \`Website visits\`, and some legacy actions also show primary-for-goal at account level. In the local campaign, the 24 local micro-actions appeared in \`All conversions\`, not \`Conversions\`, suggesting campaign-goal selection limits actual effective counted goals. **Inspect campaign-specific goals in UI**; never infer from global \`primary\` flag alone.
- Call conversion reporting counts calls meeting a set threshold or approved AI-qualified calls, not necessarily answered appointment/visit. Exact duration threshold, caller status, call recordings settings, duplicate calls, clinic answers, and outcome remain unverified.
- The connector offers no confirmed edit-conversion-action workflow. Google Ads UI: Goals → Conversions → Summary → \`Calls from ads\`: inspect counting, primary/secondary, minimum call length, recording setting and attribution; campaign Settings → Goals: verify which effective campaign goal was actually used. Do not delete call conversions: measurement is not a separate conversion fee.
- Offline \`visit_completed\` design is already implemented in first-party DB with GCLID/GBRAID/WBRAID + internal attribution, deterministic dedupe, and Google Data Manager validate-only passed; **first genuine paid completed-visit live import, replay and reconciliation still not proven**. Require real clinic outcome data and privacy-safe import without PHI. In clinic logs record date/time, ad-source if available, answered/missed, eligible patient, requested/confirmed/completed, collected revenue and contribution. Do not rely on platform call counts as patients.
- For website telephone clicks: \`tel:\` links are present, but they do not prove connected calls or Google Ads source. Website call-conversion dynamic forwarding tag/approved telephony integration is not shown in current frontend source; investigate regulatory and call-recording constraints before adding. Keep clinical data out of marketing tags.
- GA4 deliberately uses production-only allowlist (/about, /contact, /privacy, /terms, /accessibility, /notice-of-privacy-practices) rather than clinical/booking pages. Connected GA4 returned only three direct sessions (Nov 3–4) and is **not a full-funnel paid landing or booking monitor by design**. First-party booking attribution and office outcomes are primary. Audit API receipt and Data Manager, not simply add generic GA4 tags on sensitive health pages.

## 5. Website, offer, operations and compliance

- **Implemented/staging accepted:** responsive mobile/tablet menu, visible phone and booking CTA at small widths, fallback mobile quick bar on pages missing it.
- Homepage/site code includes actual \`tel:+13104670101\`, dedicated urgent and traveler landings, booking link and clinic-hour/911 boundary. Booking JS posts an appointment request, initial status is pending rather than confirmed.
- Critical commercial UX: verify API availability slots, service names, booking completion, no accidental duplicate submission, responsive call CTA and cookie overlay at 320/375/680/768/1024px, and first-party \`gclid\` preservation through click→booking→pending/confirmed/completed. Run real device/synthetic testing; source code is not proof of live performance or Core Web Vitals.
- **Price disagreement** as above. Site terms and Notice of Privacy Practices source contain conspicuous draft/placeholder text and explicitly await clinic/legal approval. Treat as high priority credibility/legal/policy review; do not overwrite with generic invented legal text.
- Existing Page / Contact / insurance copy makes claims like Medicare accepted, same-day when available and selected hotel visits: verify current clinic facts, hours, coverage, consent before promoting; keep pricing exact.
- Distinct traveler landing offers hotel visit conditionally, uses pre-arrival \`/book?service=traveler-care\`. Traveler Search is nationwide US geo, unlike local campaign; that is intentional pre-arrival, but too broad without observed outcomes. Start with demonstrably traveler-specific terms, avoid generic concierge/telehealth/refills, and verify real operational capacity. Traveler campaign has no delivery data, **not evidence of failure**.
- GBP and Search Console are valuable adjacent local demand channels. Source GSC data Oct 15–Nov 7 show \`urgent care near me\` 124 impressions/2 organic clicks/average position ~9.26, \`urgent care beverly hills\` 51/1/position ~11.73, \`medical clearance for surgery near me\` 36/0/position ~4.14. Organic presence plus paid suggests landing relevance improvements and separate pre-op growth opportunity. GSC is not paid conversion measurement. GBP reporting has lag/sparsity after Nov 4; do not interpret these as confirmed zero calls.
- Google healthcare advertising restrictions matter even for seemingly benign ad destinations if linked pages facilitate online prescription services. Keep in-person/local urgent pilot assets policy-isolated and don't misrepresent actual service. As of official notice posted Nov 4, 2026, new NABP accreditation option for telemedicine certification in US/UK/Canada is scheduled to be introduced in Nov; confirm actual effective policy and clinic eligibility before any telemedicine advertising. Do not silently assume LegitScript mandatory exclusively. Current clinic choice defers certification.
- Health-based remarketing/Customer Match/audience personalization, indiscriminate recording or sending PHI to ad systems are not default optimization levers. First-party nonclinical attribution is appropriate within applicable rules.

## 6. Recommended optimization strategy, ordered

**P0 — prior to relaunch (operational integrity and data correctness):**
1. Confirm production \`main\` Jenkins/smoke, mobile booking + call CTA, live appointment API, clinic phone pickup, accessibility, legal copy status and correct price. Unverified production runtime is a gate.
2. Clinic chooses maximum actual test spend and budget horizon; \`$10/day\` + \`$5/day\` are **average** daily budgets, NOT a hard combined $15 daily ceiling. Google commonly allows 2× on a day and ~30.4× monthly, subject to changes; use a hard end date / account spend controls and monitored stop conditions if strict cap required.
3. Google Ads UI read: \`Calls from ads\` exact duration/counting/goal; campaign-specific goal; call detail log and any approved recording/privacy condition; confirm call asset & location asset current delivery/policy. Match the 9 reported calls to nonclinical business outcomes; classify recurring callers, answered, booked, completed.
4. Resolve ad/site price mismatch; do not make unsupported walk-in, 24/7 or insurance promises. Align headline and landing. Fix legal/NPP placeholders through clinic/legal approval.
5. Validate GCLID/session → booking → appointment → completed → Google Data Manager import/dedupe; don't promote diagnostic micro-conversions to Smart Bidding goals. Maintain call reporting rather than deleting it.

**P1 — controlled next learning experiment, only after Dr. Farah's explicit spend authorization and policy review:**
6. Start with single focused in-person Urgent Care Search test at $10/day average (or lower separately approved), keep exact/phrase local-intent Beverly Hills group as primary; leave poor Near-Me group PAUSED until independently justified. Keep generic competitor/pediatric/insurance mismatch negatives precise and monitor close variants.
7. Test medically accurate, differentiated RSA copy: physician-led clinic, Beverly Hills, specific hours, same-day only when available, accurate price, direct phone/booking; approved sitelinks, structured snippets, location assets; no broad expansion or unverified generic location/prescription assets.
8. Diagnose granular Quality Score components, search terms, impression share by intent, click device and real call/booking quality after every 20–30 paid clicks or weekly review (sample threshold is an operating heuristic, not Google rule). Stop terms with sustained cost and no verified patient interest. No blanket pause for all \`near me\` traffic, but don't spend ~57% there again with no evidence.
9. Budget should not be split across traveler at first unless separately justified; zero-impression traveler test has no performance history. If traveler later enabled, time-bounded pre-arrival experiment with separate destination, US geo but high-intent traveler/hotel keywords and capacity, strict finite budget.
10. Keep manual CPC while reliable business-conversion signal volume is insufficient; only then test automated \`Maximize conversions\` / tCPA using verified qualified leads/visits, controlled experiment, and stable import quality. Do not optimize to local Directions, Website visits, phone clicks or all 'primary' micro-actions.

**P2 — strategic growth and learning:**
11. Build KPI dashboard: paid cost, clicks, CTR, search queries, call answered/qualified rate, online booking created/confirmed, completed visits, source-matched CAC, contribution margin; monitor by intent/ad group/device/day.
12. Improve mobile landing above-fold clarity, clinic hours/location, verified service/price and differentiated value vs large chains, in-page scheduling CTA, page speed/LCP/CLS (real PSI/Core Web Vitals tests), and split eligible pre-op / traveler / urgent messages. Track consent-safe **diagnostic** funnel locally.
13. Integrate GBP (accurate categories/services, UTM'd website links, real reviews, photos, hours/location) and Search Console content improvement; avoid broad retargeting for health-specific audiences. Investigate high-value pre-op clearance as a separate future channel once economics/policy and accurate service page are verified.
14. Consider Search AI features only when their query coverage, creative and privacy restrictions can be controlled and measured. PMax/Display/Demand Gen and AI/ChatGPT ads are separate experiments, not an automatic efficiency improvement for this current limited dataset.

## 7. Explicit data gaps / verification checklist

- **DATA_GAP:** exact duration threshold and status of each of the 9 calls, verified appointment count, new vs returning, completed visits, revenue/margin, campaign-specific conversion goals.
- **DATA_GAP:** updated fresh readback of 5 added negatives; cached search data omitted latest mutations.
- **DATA_GAP:** PageSpeed/Core Web Vitals, live production site response, phone call answer handling, booking-path real-device tests; automated site fetch unavailable through current environment.
- **DATA_GAP:** final counsel-approved Terms/NPP, insurance/Medicare operational facts, traveler capacity/arrival area, call asset recording/HIPAA handling and policy resolution.
- **DATA_GAP:** current exact main/dev Jenkins branch success after 2026-11-07 merges; both were pending at review start.
- **DATA_GAP:** end-to-end \`visit_completed\` Data Manager recording, replay/deduplication and Ads reconciliation.

## 8. References

Google official:
- https://support.google.com/google-ads/answer/10995103 (primary vs secondary)
- https://support.google.com/google-ads/answer/9143218 (campaign goals)
- https://support.google.com/google-ads/answer/6095882 (calls from ads)
- https://support.google.com/google-ads/answer/6100664 (call conversion types)
- https://support.google.com/google-ads/answer/2453972 (negative keywords / variants)
- https://support.google.com/google-ads/answer/6385083 (daily budgets)
- https://support.google.com/google-ads/answer/6167118 (quality score)
- https://support.google.com/adspolicy/answer/176031 (healthcare policies)
- https://support.google.com/adspolicy/answer/18794834 (NABP Nov 2026 announcement)

This report is an evidence-backed technical operating audit. Approved business decisions remain solely in \`docs/DECISIONS.md\` and live account actions require separate authorization.
