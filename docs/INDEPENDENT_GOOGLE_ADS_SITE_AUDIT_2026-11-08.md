# Independent Google Ads and Website Audit — Dr. Farah

**Audit date:** 2026-11-08  
**Scope:** Google Ads 652-510-3588; repository code dev; business/measurement specifications; Google Search Console, GA4, GBP connectors; Google official help and policy documentation.  
**Authority:** Live connector for account data; code for implementation, not live browser QA. No launch/spend/targeting/conversion settings changed in this audit. Current source of truth: PROJECT_HANDOFF.md and ROADMAP.md.  
**Evidence convention:** FACT directly verified; HYPOTHESIS testable; DATA_GAP not established; RECOMMENDATION proposed, not approved.

## Executive finding

The first five spending days of a local urgent-care Search pilot were neither demonstrably successful nor demonstrably wasted. Google generated real ad engagement (68 clicks) and reported 9 calls, with 3 ad-call conversion events, at $281.67 cost. There is **zero verified linkage in the available read** between those events and a confirmed appointment, completed patient visit, or collected revenue. The best immediate optimization is **quality and attribution**, not a blanket deletion of conversions or automatic scaling.

Search intent was fragmented: the "Near Me" group absorbed 57% of campaign spend with zero reported ad-call conversions, while 3 platform ad-call conversions came from the Beverly Hills group. 89% of spend occurred on mobile. These are directional samples only. Already-implemented restrictions: Near Me ad group PAUSED, both Search campaigns PAUSED, daily configured budgets reduced $40->$10 and $20->$5, 5 competitor/location negatives added to local Search.

## 1. Live Google Ads, 2026-11-02 through 2026-11-06

| Measure | Observed |
|---|---:|
| Impressions | 2,271 |
| Clicks | 68 |
| CTR | 2.99% |
| Cost | $281.67 |
| Average CPC | $4.14 |
| Google-reported phone_calls | 9 |
| "Calls from ads" counted conversions | 3 |
| Cost per counted ad-call conversion | $93.89 |
| Cost per reported phone call (descriptive, not qualified) | $31.30 |
| All conversions | 27 (3 ad calls + 8 Directions + 15 Other engagements + 1 Website visit) |
| Search impression share | 24.95% |
| Search lost impression share (budget) | 48.92% |
| Search lost impression share (rank) | 26.13% |

The $10/day setting is an **average** budget, not an absolute per-day spending ceiling; Google may spend up to 2x on a day for many campaigns. Official: https://support.google.com/google-ads/answer/10486637 . Neither the $93.89 event cost nor any prior $281.67 spent is an extra "conversion charge". Google Ads cost is media delivery/interaction spend.

| Ad group | Clicks | Spend | Calls-from-ads conversions | Current readback status |
|---|---:|---:|---:|---|
| Urgent Care / Beverly Hills | 23 | $101.93 | 3 | ENABLED at ad-group level; parent campaign PAUSED |
| Urgent Care / Near Me | 40 | $160.09 | 0 | PAUSED at ad-group level |
| Walk-In / Same-Day | 5 | $19.65 | 0 | ENABLED at ad-group level; parent campaign PAUSED |

61 of 68 clicks and $251.10 of $281.67 were MOBILE; desktop 6/$26.10, tablet 1/$4.47. Google Search Partners reported 131 impressions and zero clicks/spend, while latest settings indicate partners disabled. This may reflect a historical configuration/reporting window: verify before attributing waste.

The three observed calls-from-ads conversions were not validated against answered-call logs or business outcomes. Do not claim 3 patients, 3 qualified contacts, 3 appointments or ROAS.

## 2. Search intent and negative keywords

The query "urgent care near me" generated 20 clicks / $78.34 / 0 platform conversions. Generic "urgent care" 5 / $21.50 / 0. Competitor-targeted "cedars urgent care wilshire" 6 / $26.80 / 1 platform call conversion (not a proven completed visit). Exact legitimate Beverly Hills intent showed fewer clicks; small sample. Google allows close variants even on Exact/Phrase.

Already added: negative PHRASE "cedars urgent care", "exer urgent care", "excer urgent care", "kaiser urgent care"; EXACT "8767 wilshire blvd urgent care". Write was accepted; immediate readback through cached data did not establish persistence, so recheck in Google Ads UI.

RECOMMENDATION: Keep Near Me paused until a bounded dedicated experiment demonstrates qualified patient value. Keep highly local phrase/exact intent grouped by true offer. Review Search Terms weekly and add irrelevant competitors, pediatric-only, emergency department, insurer-only, free/after-hours etc **only after** clinic eligibility/service scope validation. Do not broad-negate "near me" across all campaigns or exclude people seeking valid care. Avoid blanket brand exclusion until lead outcomes are checked.

## 3. Conversion configuration — precise diagnosis

Live account conversion actions: "Calls from ads" (AD_CALL / PHONE_CALL_LEAD / enabled / Primary / MANY_PER_CLICK), "Local actions - Directions" (GET_DIRECTIONS / Google-hosted / Primary / MANY_PER_CLICK), "Local actions - Other engagements" (ENGAGEMENT / Google-hosted / Primary / MANY_PER_CLICK), "Local actions - Website visits" (PAGE_VIEW / Google-hosted / Primary / MANY_PER_CLICK).

Campaign Conversions counted 3 Calls from ads; other actions appeared in All Conversions. Therefore **Primary at the action's goal is not sufficient to prove the campaign uses it for bidding**. Google's goal logic requires both Primary action and selected campaign goal (see https://support.google.com/google-ads/answer/10995103). Current pilot is Manual CPC, with enhanced CPC disabled; thus no evidence that automated Smart Bidding wasted money chasing low-value conversions.

"Calls from ads" uses call reporting, and conversion counting may depend on a configured minimum duration: https://support.google.com/google-ads/answer/6095882 . Phone_calls and conversion counts are not the same. The current count setting MANY_PER_CLICK can count multiple call leads from a single ad interaction. Lead action counting often should be "One" rather than "Every" for a unique lead (see https://support.google.com/google-ads/answer/3438531). This is a **recommendation to inspect/change**, not a confirmed error about actual duplicates.

**Needed Google Ads UI inspection**: Goals -> Conversions -> Summary -> Calls from ads -> Edit settings. Check minimum call duration, Count (prefer One per ad interaction for lead measurement), action optimization Primary/Secondary, value and windows. Then Campaigns -> local pilot -> Settings -> Conversion goals: confirm which exact goals are selected. Keep Directions/Website visits/Other engagements observation-only for business optimization where configurable; avoid accidentally bidding on them in a custom goal. Do not delete historical measurement. No supported Windsor action edits conversion action goals/count; browser UI or a separately approved direct Google Ads API integration with appropriate scopes is required.

Call reporting and call conversion reporting enabled; default call conversion resource \`customers/6525103588/conversionActions/179\`. No reliable call-by-call duration/answer status or clinic outcomes returned by available connector fields. Avoid recording patient conversations until approved with appropriate healthcare privacy/compliance analysis. Reconcile non-clinical phone billing and scheduling records to report call answered -> appointment requested -> confirmed -> completed.

## 4. Geography, budget, scheduling and bidding

Local campaign: 5-mile proximity around Beverly Hills, positive geo mode PRESENCE, regular weekday clinic schedule Mon-Thu 08:30–17:30 and Friday 08:30–16:30; Manual CPC, enhanced CPC OFF; Search partner and Display targeting OFF on latest readback. Budget now $10/day PAUSED. Ad groups above.

Traveler campaign: US geo and planned advance/traveler demand, separate policy-isolated landing and $5/day PAUSED. Zero traffic in measured test; no performance conclusion. Traveler national reach can be valid for pre-arrival travel intent, but requires explicit pre-arrival/traveler wording and genuinely available hotel or clinic care.

Large search lost impression share (budget ~49%) does not justify increasing bids or budgets when the most costly ad group has no proven patient outcome. At 10/day and ~$4.14 CPC one should expect only around 2–3 clicks on an average spending day with a similar mix, not statistically conclusive daily results. An average budget of $10+$5/day across 30.4 days would imply ~$456/month if consistently active, but schedules and mid-month changes affect actual billing; each campaign may spend up to 2x its average on an individual day. Confirm actual account spend, third-party Local Services campaign and budget alerts separately if there is a strict all-account maximum. Do not infer historical budget overspend from a day above average.

Future local launch if explicitly approved: start with already-proven Beverly Hills group only, stay Manual CPC or comparable cap with no blind Target CPA/Maximize Conversions until robust qualified outcomes. Monitor cost/answered call, appointment request, completed visit, and estimated/actual margin. Stop on unacceptable confirmed CAC, systematic irrelevance, missed calls or a site/booking outage. Once stable meaningful completed-visit data accumulates, test automated bidding on **true business outcomes**; do not switch prematurely for 3 ad-call events.

## 5. Ad copy, ads/assets, and policy

Current Urgent Search RSAs show ad-strength AVERAGE/AVERAGE/POOR; Traveler pilot GOOD/GOOD/AVERAGE (strength is diagnostic, not profitability). Ad copy in Urgent RSAs includes "Urgent Visit From $250"; landing /urgent-care-beverly-hills and business source state starting $240. **Action:** resolve authoritative approved price and change either copy or page consistently; no fabricated offer. "Walk-In Urgent Care" ad can imply guaranteed walk-ins, but the website only requests an appointment pending clinic confirmation. **Action:** determine true walk-in policy; if not walk-in, replace walk-in headlines and keyword theme with "Same-Day Appointment Request" or accurate availability language. Ads currently include appropriate "Same-Day When Available" language.

Certification-sensitive ads/assets documented: prescription drug / virtual prescribing / telehealth assets were disapproved; relevant future services subject to Google's US healthcare/certification requirements. The clinic previously deferred LegitScript for the current policy-isolated in-person local/traveler Search experiment; do not circumvent policy by misrepresenting services. A clinic call asset had compliance/supplemental-terms issues; reconcile approved recording/monitoring settings and status before relying on it. Official https://support.google.com/adspolicy/answer/176031 and https://support.google.com/adspolicy/answer/16701855 . Sensitive health audiences, Customer Match and remarketing are not blanket growth levers.

## 6. Paid landing + site audit

Responsive header/menu and persistent Call/Book navigation were corrected in PR #128 and approved visually on staging, then merged to main PR #129; production main branch Jenkins successful, but independent live production viewport/functional smoke still needs evidence. This fix is especially meaningful because 89% of ad spend was mobile.

Urgent landing has physician-led same-day *when available*, office location, weekday hours, explicit non-ER distinction, starting price $240, book/call CTA, and supported outpatient services. Traveler landing is tailored to advance care for visitors; hotel/mobile visits conditional on availability/clinical suitability. Booking flow requires service -> availability -> slot -> personal details -> submit and produces a **pending** request, not a confirmed visit. Phone-first pre-op exception remains. Important UX proposals: above-fold transparent current offer, clear clinic type and exact location, no unnecessary choice overload, no false 24/7/walk-in promise, backup phone when dates unavailable, test all booking steps at 320/375/768/1024px and slow 4G.

**HIGH PRIORITY content/legal finding:** repository source \`frontend/terms.html\` still labels its content a draft/placeholder awaiting clinic/legal approval; \`frontend/notice-of-privacy-practices.html\` explicitly calls the HIPAA NPP content a placeholder. This is a real source-code finding; live remote URL could not be inspected in this environment. Clinic/legal must provide approved publication-ready content. Do not claim legal noncompliance from code alone or invent legal text.

Site \`frontend/analytics.js\` loads GA4 only on safe public informational pages, intentionally not on homepage, paid health-intent landings, booking and registration. GA4 connector showed 3 direct sessions across Nov 3–4 from an Oct 15–Nov 7 read, **not proof of only three total site visits**. Core paid performance cannot be inferred from GA4 sessions. First-party \`frontend/app.js\` captures UTM/GCLID/GBRAID/WBRAID and \`frontend/booking.js\` submits attribution together with new pending appointments via API. The code path exists; first genuine click -> pending booking -> confirmed -> completed -> deduped offline import and Ads reconciliation is NOT live-validated. Preserve staging/production isolation and exclude sensitive clinical free-text and PHI from advertising payloads.

## 7. Organic + GBP cross-check

Search Console data Oct 15–Nov 7 showed organic interest in "urgent care near me", "urgent care beverly hills", "medical clearance for surgery near me"; organic landing queries can guide paid keyword and SEO copy, but **organic click/position is not an Ads conversion metric**. Legacy URL impressions (e.g. old blog or /about-us/, /services/ aliases) remain visible in GSC; audit redirects/canonicals, avoid incorrectly assuming these pages are current live production endpoints. GBP records have calls/directions/website actions, but should not be added to Google Ads call counts: they can overlap/reflect different scopes and are not necessarily resulting in visits. GBP review count showed inconsistent source aggregation (one row count=1/5.0 vs historical 109/5.0 baseline); do not present as current verified total without checking profile entity.

## 8. Priority-based strategy

**P0 before any restart:** (1) Resolve actual ad call dispositions with reception (9 reported calls), avoid PHI; (2) remove $250 vs $240 discrepancy and walk-in claims unless true; (3) inspect Google Ads Calls from ads goal/count/duration and campaign-selected goals, change only with permission; (4) obtain approved legal NPP/Terms and reconcile call asset requirements; (5) production mobile booking and fallback phone smoke, ensure no API/cookie errors; (6) verify five negative keywords in UI and ensure paused statuses/budgets unchanged.

**P1 — finite local experiment after explicit Dr. Farah launch/spend approval:** prioritize precise Beverly Hills geographic intent, keep Near Me paused, cap $10/day average or approved figure, Manual CPC while outcomes sparse, search terms/negatives review after real clicks, use patient outcomes and 7-day rolling evidence rather than same-day vanity metrics. Separate brand, urgent local and other services only if learning budget can support meaningful data; avoid account fragmentation into many tiny campaigns.

**P2 — reliable business attribution:** keep authoritative first-party appointment status and deduplicated visit_completed import, clinic source mapping for directly dialed phone calls, daily/weekly reconciliation of paid clicks/calls/bookings/completed visits; report CAC and contribution once collected revenue/cost available. Website-side CTA click can be useful internally but not a primary Ads outcome.

**P3 — staged expansion:** Pre-Op medical clearance search/referral based on economics and separate approved service landing; Traveler/Hotel pre-arrival pilot after offer/fulfillment confirmed; GBP local SEO + reputation; physician video and hotel/physician referral; ChatGPT Ads only subject to current healthcare eligibility and compliance. Avoid broad PMax, AI Max, Display, health-sensitive remarketing, automated expansion or generic LA-wide search until verified incremental demand and cost quality.

## 9. Verification / ownership and stop conditions

- Clinic: actual price, walk-in/child/insurance service policy, approved NPP/Terms, call answering and operational scheduling, collected revenue/variable cost, treatment capacity, call privacy/legal review, restart authority.
- Ads operator: verify conversions goals and One/Every duration, keyword negative write readback, network/geo schedule, asset approvals and call compliance, no unauthorized spend.
- Web/engineering: complete production responsive/booking smoke, protect click ID through /book, confirm no staging pollution, first completed paid visit import/dedupe and reporting.
- Weekly dashboard: spend, clicks, answerable calls, qualified contacts, confirmed bookings, completed visits, cancellations/no-shows, CAC per completed visit, gross contribution, query quality, source confidence.

**Explicit decision:** This document is analysis, not a decision to enable/expand Google Ads, change conversion goals, accept recording terms, or submit unapproved medical/legal copy.
