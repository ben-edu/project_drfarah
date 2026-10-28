# Google Growth Audit — Ads / Search / GBP / GA4

**Date:** 2026-10-28

This is an execution audit, not a one-time report. Live systems remain authoritative for current state.

## Google Ads

### Legacy paid history

- Smart campaign `Urgent Care Medical Center` (`22552983079`) is paused.
- Historical activity: June 2025–February 2026.
- Approximate totals: 258,541 impressions, 5,590 clicks, $4,494.86 spend, 16 platform conversions.
- The old conversion signal is effectively calls from Smart Campaign ads, not completed visits.
- Mobile dominated the old paid activity and reported conversions.
- Geography showed waste outside the intended service area, including paid traffic in Brentwood in Northern California without conversion value.

Action: retain forensic evidence; do not use old platform conversion counts as the new optimization target. Do not relaunch the Smart campaign by default.

### Local Services campaign

A second system-generated campaign exists:

- ID `23637947414`;
- `LocalServicesCampaign:SystemGenerated:00064c99af1b40d4`;
- account status ENABLED / primary status ELIGIBLE;
- bidding-system status PAUSED;
- no impressions, clicks or spend in the inspected recent 90-day window.

Action: leave unchanged until its account/platform role is fully understood.

### New Search pilot

Created paused as campaign `24414014329`. See `docs/GOOGLE_ADS_PILOT_2026-10-28.md`.

No spend has started.

## Search Console

Property: `sc-domain:drfarahvipurgentcare.com`.

Recent 90-day live read on 2026-10-28:

- ~32,325 impressions;
- 308 clicks;
- CTR ~0.95%;
- average position ~11.8.

Current opportunity signals include:

- `urgent care near me`: meaningful impressions around average position ~15;
- `urgent care beverly hills`: meaningful impressions around position ~10.5;
- `beverly hills urgent care`: meaningful impressions around position ~15.8;
- branded terms are much stronger and generally rank near the top.

Old WordPress URLs continue to appear in historical Search Console rows. The production Apache config already has 301 rules for several important legacy paths. The correct action is live redirect/canonical verification, not blindly recreating old pages.

High-value redirect improvement prepared in this batch:

- `/urgent-care-near-you` → `/urgent-care-beverly-hills`;
- `/vip-urgent-care` → `/urgent-care-beverly-hills`.

The new canonical urgent-care page is added to sitemap. `/book` and `/patient-registration` remain outside the sitemap and noindex under the current architecture.

## Google Business Profile

Connected location: `locations/6719840585856592244`.

Captured profile baseline:

- Dr Farah VIP Urgent Care;
- primary category `Urgent care center`;
- rating baseline 5.0 / 109 reviews at capture.

Recent 90-day live profile performance:

- ~120 website clicks;
- ~123 call clicks.

Current live clinic hours:

- Mon–Thu 08:30–17:30;
- Fri 08:30–16:30;
- Sat–Sun closed.

Clinic geo used for Ads proximity: 34.067, -118.3934.

Audit issues:

- `has_google_updated=true`: inspect Google-applied/suggested profile updates before accepting profile state as final;
- stale special-hours entries from 2025 need review/removal/replacement with current holiday hours as appropriate;
- service catalogue contains duplicates and some overly aggressive marketing wording; clean item-by-item rather than bulk-delete;
- Ads messaging and schedule must match actual GBP hours; do not advertise 24/7 availability.

## GA4

Production property:

- property `489069776`;
- web stream `11211773871`;
- measurement ID `G-D58FTMF05S`.

The repository contains the approved selected-page production architecture. Recent Windsor reads returned no GA4 rows for the inspected period. This does not by itself prove the tag is broken; live Realtime/DebugView and settings should be verified directly.

Pending validation:

- one safe allowlisted production page view;
- timezone/currency;
- Enhanced Measurement state;
- consent behavior;
- confirmation that excluded sensitive pages do not receive unintended analytics measurement.

The new urgent-care landing page should remain outside the current GA4 allowlist. Paid-source linkage is handled by first-party click/source attribution and the completed-visit feedback path, avoiding unnecessary health-context analytics collection.

## Cross-channel operating model

Use each system for the job it is best suited for:

- Google Ads: paid search delivery and optimization feedback;
- Search Console: organic Google query/page truth;
- GBP: local/Maps presence, calls, website actions, factual profile state;
- GA4: approved low-risk behavioral diagnostics;
- first-party database: click/source → booking → appointment linkage;
- Data Manager: completed-visit outcome feedback to Google Ads.

Do not force all data into one Google product and do not duplicate sensitive measurement merely because a platform supports it.

## Immediate execution queue

1. deploy and smoke-test the new urgent-care landing page;
2. change Google Ads target-location option to presence-only before campaign enable;
3. create responsive search ads against the live landing page;
4. validate Data Manager destination/auth path;
5. promote the Data Manager runtime batch to production after acceptance;
6. inspect GBP Google updates, stale special hours and service duplicates/claims;
7. verify GA4 live receipt/settings;
8. begin the paid pilot only after the launch blockers in the pilot spec are green;
9. use first real paid completed visit for the controlled offline conversion import;
10. then implement durable import ledger/scheduling/retry/monitoring.
