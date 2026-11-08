# Production responsive mismatch — release QA and recovery

Status: OPEN P0 production-serving incident, 2026-11-08. GitHub Issue #134. ROADMAP.md section 3A P0-01 is the authoritative execution plan.

## Confirmed

Staging mobile/tablet Call, Book and menu UX was visually accepted by the operator. Production did not show the same changes after PR #129 reached main and Jenkins reported success. Git main contains the correct JavaScript and CSS; the previous Jenkins smoke only grepped "Dr. Farah" on the served homepage, which does not uniquely identify the new site. Staging HTTP cache policy had no-store; production only no-cache/must-revalidate. Most pages loaded unversioned app.js and styles.css. Therefore earlier CI success did not prove the public origin returned the correct assets.

## Unverified root cause

Browser cache, CDN or proxy cache, incorrect production DNS/HAProxy origin, different Hestia document root or deploy skipping remain possibilities. Do not assume one until served bytes/headers and Jenkins deploy stage logs are compared.

## Remediation implemented

- All 21 HTML source pages request versioned app.js and styles.css (v=20261108-mobile2).
- Home page HTML provides marker mobile-nav-20261108-2.
- Production Apache temporarily disables HTML/CSS/JS storage during investigation.
- Production Jenkins deployment smoke now checks the marker and compares the exact bytes of public production app.js and styles.css against the built release files. Failure means release NOT verified and requires infrastructure/cache diagnosis; no blind retries.

## Acceptance

1. Feature PR passes exact-head CI. Merge dev and confirm staging still correct on 320, 375, 680, 768 and 1024px; Call 310-467-0101 and Book work on Home, Urgent Care, Traveler, Book and Pre-Op.
2. Before dev-to-main release, verify clean branch ancestry and full diff; get explicit staging acceptance for changed cache references if visual behavior changed.
3. Main Jenkins must pass the exact public release marker/asset-content checks, not just generic HTTP status.
4. If check FAILS, inspect live DNS, proxy upstream, Hestia docroot path and file hash, response headers (Age, Cache-Control, ETag, CF-Cache-Status), browser cache and possible service worker. Fix infrastructure through approved ops path; this source patch alone cannot repair external DNS.
5. If check PASSES, independently verify production actual device/browser behavior and record SHA, headers, URLs and acceptance in Issue #134 before closure.
6. Never mark fixed based solely on merge commit or generic Jenkins green.
