# Dr. Farah — cost containment and responsive conversion path audit

Date: 2026-11-07. Sources: live Google Ads account via Windsor.ai, GitHub frontend code and prior approved project handoff/decisions. This is dated evidence, not a replacement for ROADMAP.md.

## Live Google Ads actions (confirmed)

Account 652-510-3588.

- Local Search 24414014329: PAUSED; daily budget changed from USD 40 to USD 10, subsequent live budget readback USD 10.
- Traveler Search 24404901753: PAUSED; daily budget changed from USD 20 to USD 5, subsequent live budget readback USD 5.
- Legacy Smart 22552983079: PAUSED, no write.
- Google-managed Local Services 23637947414: ENABLED with 0 reported cost in the examined time window, not modified. Validate its billing/delivery separately before assuming all account spend is capped by the two Search budgets.
- Local Search in 2026-10-28..2026-11-07: 68 clicks, USD 281.67 cost, 3 primary campaign Conversions, all reported as "Calls from ads"; all-conversion event breakdown includes 8 directions, 15 other engagements, 1 website visit and 3 ad calls. No proof of patient visits.
- Narrow negative keyword additions to local Search succeeded: [PHRASE] cedars urgent care, exer urgent care, excer urgent care, kaiser urgent care; [EXACT] 8767 wilshire blvd urgent care. Avoid broad exclusions that may remove legitimate urgent-care patients.
- Search terms within period: "urgent care near me" 20 clicks / USD 78.34 / 0 platform Conversions; "cedars urgent care wilshire" 6 clicks / USD 26.80 / 1 platform Conversion. Because the latter is competitor-branded, it was excluded as a controlled budget-quality measure, not because its primary Conversion was proven fake.

## Measurement interpretation and next verification

Google Ads identified four enabled conversion actions: "Calls from ads" (PHONE_CALL_LEAD, primary for goal), "Local actions - Directions" (GET_DIRECTIONS, primary-for-goal property), "Local actions - Other engagements" (ENGAGEMENT, primary-for-goal property) and "Local actions - Website visits" (PAGE_VIEW, primary-for-goal property). Campaign Conversions included only 3 Calls from ads in observed time; other local events appeared in All Conversions. Do not assume any event equals a booked, connected or completed patient. The two current Search campaigns use Manual CPC; platform conversion goal configuration must be checked before moving to automated bidding.

The connected Ads write interface has no conversion-action editing action. Do not disable measurement or erase historical data: inspect Call details (duration, connection status), call qualification and clinic scheduling log with non-clinical attribution. Preserve call-recording privacy/compliance constraints. Intended final business outcome is validated visit_completed.

## Responsive site issue and fix scope

Before this change, CSS hid primary navigation at <=1040px and showed the bottom quick action bar only at <=680px. At <=600px it hid the header phone button. The website thereby lacked reliable responsive navigation and persistent visible number/Booking across paths.

This change adds a keyboard-accessible JS menu toggle and mobile dropdown (escape/outside click closure, aria-expanded, scrollable overflow), readable tablet header phone, always accessible mobile bottom number + Book/phone-scheduling CTA, and a fallback mobilebar on pages that omitted it. Booking wizard receives an in-page booking anchor rather than a reload link.

Validation required before production claim: JS runtime and click/keyboard checks; 320, 375, 680, 768, 1024 desktop/tablet/mobile widths; homepage + urgent-care + traveler + booking pages; no horizontal overflow; correct tel:+13104670101 and /book targets; correct pre-op phone-only exception; check sticky bottom bar safe area/cookie banner; branch CI -> dev staging -> main Jenkins -> production smoke.

## Current next actions

1. Validate and merge the responsive fix to dev, then release to main only after exact-head green CI, complete main..dev review and proper staging QA.
2. Obtain authoritative Google Ads Call details and clinic non-clinical phone/appointment reconciliation for the three ad calls.
3. Inspect current conversion goals and phone asset policy in Google Ads UI; do not equate Calls from ads or Directions with completed patients.
4. Keep local and traveler Search campaigns PAUSED pending these readiness checks and a new explicit launch decision.
