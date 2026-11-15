# Google Ads restart spend and local intent audit — 2026-11-15

**Account:** 652-510-3588; USD, America/Los_Angeles. Data from connected Google Ads through Windsor.ai; historical performance (served cost) is not the billed-cost ledger. No Google Ads settings were changed in this audit.

## Restart performance (Nov 9–15; last spending date Nov 13)

Urgent Search **$189.83, 51 clicks, 1,148 impressions, 16 phone_calls, 6 Calls from ads conversions, 55 All Conversions**. Approx $3.72 CPC and $31.64 per counted ad-call conversion, not per patient. Traveler Search $0, enabled $5/day. Whole Nov 1–15 pilot **$471.50, 119 clicks, 3,419 impressions, 25 phone_calls, 11 counted ad-call conversions, 89 All Conversions**; 89 includes directions/profile actions/call clicks, not patient visits.

| Date (LA) | Cost | Clicks | Phone calls | Ad-call conversions |
|---|---:|---:|---:|---:|
| Nov 9 | $17.26 | 4 | 6 | 4 |
| Nov 10 | $20.23 | 5 | 2 | 0 |
| Nov 11 | $8.38 | 2 | 0 | 0 |
| Nov 12 | $71.98 | 19 | 4 | 2 |
| Nov 13 | $71.98 | 21 | 4 | 0 |
| **Total** | **$189.83** | **51** | **16** | **6** |

**P0 budget drift:** Urgent average daily budget is **$36** (was authorized $10), Traveler remains $5. Nov 11 16:16 Change Event says CAMPAIGN_BUDGET amountMicros 10,000,000→36,000,000 via **GOOGLE_ADS_RECOMMENDATIONS**. This identifies the Recommendations pathway, NOT whether an operator accepted a recommendation manually or automated delivery did so. User screenshots: Auto-apply History **0 subscribed recommendation types** and no listed executions; Manage shows apparent `Remove redundant keywords` checkbox 1/7 selected but save state unknown. Do not claim Auto-apply caused budget drift. Recommend exact Urgent **$36→$10 average/day** while ENABLED; requires explicit owner approval + connector write/readback. At $36 average/day, 2x is $72 possible served daily; Nov 12/13 cost $71.98 each. Check Google Ads Billed cost, adjustments/invalid clicks, budget report, Change History actor, and independent Local Services billing. A same-day budget decrease may not immediately lower today's max because day's highest earlier budget can determine limit. Google reference: https://support.google.com/google-ads/answer/10487143 .

## Near Me / group and intent crossover

Nov 9–15: **Beverly Hills** $93.07/23 clicks/**6** counted calls/7 All Conversions/13 phone_calls; **Walk-In Same-Day** $96.76/28 clicks/**0** counted calls/48 All Conversions/3 phone_calls; dedicated **Near Me** PAUSED and $0. Walk-In's 48 All = 3 Clicks to call, 14 Directions, 28 Other engagements and 3 Website visits, not 48 patients. The search term **`urgent care near me`** triggered Walk-In and spent **$59.33/17 clicks/0 counted calls**, even while dedicated Near Me was paused. `walk in clinic near me` Exact+Phrase keywords spent a combined $95.66/27 clicks with zero counted calls. Search intent matching can include near equivalents even under Exact (https://support.google.com/google-ads/answer/7478529). Competitor terms `concentra urgent care near me` $11.16/3 clicks and `kaiser permanente near me urgent care` $3.91/1 click appear; do not automatically exclude without clinic outcome context.

Historical dedicated Near Me before pause: $160.09/40 clicks/0 counted ad calls/22 local actions (6 Directions, 15 Other, 1 Website visit). Different periods/groups cannot establish whether pausing reduced genuine patient visits. Keep group PAUSED but not deleted; seek receptionist qualified leads, booked/completed visits and credible local walk-in outcomes before bounded Exact/Phrase test. Avoid blanket `near me` negative.

## Other approved actions and dependencies

Owner confirmed actual Urgent visit starting price **$250**; Google Ads creative already says $250. This candidate fixes **exactly 3 obsolete $240 displays** in 2 static site pages (2 on urgent landing, 1 on services). No appointment/backend, GTM/GA4/Matomo, medical claims or Ads edits. Run exact PR checks, merge to dev staging after green, obtain owner visual acceptance, then normal dev→main release. Actual dynamic booking service catalog pricing not verified.

Keep existing Manual CPC, no speculative switch to Maximize Conversions, no automatic broad-match/budget increase. Google Ads recommendations may be shown without Auto-apply. Matomo full implementation remains Issue #142, pending authenticated owner-service access; conversion/visit reconciliation remains P0. Current operating control and future response in Issue #110.
