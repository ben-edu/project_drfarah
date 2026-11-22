# Direct Google Ads API — read-only reporting (2026-11-22)

Status: FEATURE BRANCH / PR REVIEW. The implementation has mocked unit tests; it has NOT yet performed an authenticated Google Ads production request. No Google Ads campaigns, conversions, customer data, billing or production deployments changed.

## Existing infrastructure reused
Existing Google Data Manager authentication and service-account Kubernetes mount are preserved. Data Manager sends offline 'visit_completed' conversions; this new module reads inbound Google Ads reporting using a *different OAuth scope*. A successful Data Manager validateOnly=HTTP 200 does not demonstrate Google Ads API read permission.

Files: api/app/services/google_ads_reporting.py, scripts/google-ads-readonly-report.py, api/tests/test_google_ads_reporting.py. No new paid connectors, dependencies, cron jobs, production routes or API credentials.

## Access prerequisites
1. Identify the *existing* Google Cloud project/service account used by Data Manager. The deployment references Kubernetes secret drfarah-google-data-manager-credentials and GOOGLE_APPLICATION_CREDENTIALS=/var/run/secrets/google-data-manager/credentials.json. Never paste or commit the JSON private key.
2. In the same Google Cloud project, enable **Google Ads API**, check production API access level (Explorer or higher; Test only cannot read production Ads).
3. Ensure the service-account email appears in Google Ads account 652-510-3588 under Admin > Access and security, ideally with Read-only permission. If via a manager account, determine its login-customer-id.
4. Developer tokens were **sunset 2026-09-09**; new access is associated with the Google Cloud project. Do not block on obtaining a developer token. The Data Manager OAuth scope is NOT interchangeable with the Ads scope https://www.googleapis.com/auth/adwords.

## Operator verification (trusted runtime only)
From repository root with existing ADC safely available:

    python scripts/google-ads-readonly-report.py --report account
    python scripts/google-ads-readonly-report.py --report campaigns
    python scripts/google-ads-readonly-report.py --report budgets
    python scripts/google-ads-readonly-report.py --report daily --start 2026-11-09 --end 2026-11-15
    python scripts/google-ads-readonly-report.py --report ad_groups --start 2026-11-09 --end 2026-11-15
    python scripts/google-ads-readonly-report.py --report search_terms --start 2026-11-09 --end 2026-11-15
    python scripts/google-ads-readonly-report.py --report changes --start 2026-11-09 --end 2026-11-15

The 'changes' preset is limited to fewer than 30 days and can identify Change Event client type/actor where available. It does not independently verify Auto-apply subscription settings or billed cost (Google Ads UI authoritative). Campaign-served cost, platform conversions, calls and real completed patient visits are distinct.

## Next acceptance gate
Get actual Google Cloud API enablement, access-level and Google Ads service-account permissions verified; run account + campaigns read-only check; validate v26 GAQL on real account; inspect exact permissions/errors. Only after success run recent daily, search terms, budgets and change events. Log non-secret request IDs/evidence in GitHub. No campaign writes or unauthorized spending.

Sources: 
- https://developers.google.com/google-ads/api/docs/api-policy/developer-token
- https://developers.google.com/google-ads/api/docs/api-policy/access-levels
- https://developers.google.com/google-ads/api/docs/oauth/service-accounts
- https://developers.google.com/google-ads/api/fields/v26/overview
- https://developers.google.com/google-ads/api/docs/release-notes
