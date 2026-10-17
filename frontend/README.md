# Dr. Farah — Frontend (Phase 1, V2 dark redesign)

Static, build-free frontend. Plain HTML + CSS + vanilla JS, deployed to Hestia via
Jenkins (rsync). No build step. Dark, dramatic "quiet luxury" direction.

## Pages
index, services, about (detailed), contact, book (API-wired wizard),
privacy, terms, accessibility, notice-of-privacy-practices, 404.

## Design
Warm-noir palette (#0C1518 base), luminous bronze-gold (#C6A15B) accent,
Cormorant Garamond (display) + Inter (body). Custom SVG icons, custom stylised
SVG location map (no third-party map cookies) with a "Get directions" link to
Google Maps. Cookie banner is necessary-only with a working acknowledge button.

## API wiring (book.html + booking.js)
booking.js derives API_BASE from hostname (staging/prod), calls
GET /services, GET /availability, POST /appointments (handles 201/409/422).
Times shown in America/Los_Angeles. Until a validated ContactRequest backend
exists, the contact page offers only working phone and online-booking actions.

## Extensionless URLs
Links use /services etc. Verified working on staging: nginx proxies extensionless
requests to Apache, which honors the shipped .htaccess (AllowOverride All).
Keep .htaccess.

## Assets
The frontend uses direct local WebP files for its approved Dr. Farah/clinic
photographs. The previous Base64 runtime reconstruction, broken WebP files and
unused generic AI placeholders have been retired. Keep the source image bytes
intact and verify that every WebP decodes after upload. The IV photograph used
in the Services and IV heroes is only 500×281; a sharper original from the
clinic is still needed to improve its large-screen quality.

The legacy WordPress insurer-image hotlinks were removed before production.
The launch version uses the accessible named insurance text cards already in
the HTML. Approved local artwork can replace them later without adding a
runtime dependency on the old host.

## Legal / noindex
Legal pages remain drafts pending clinic and counsel review. Source HTML carries
`noindex,nofollow,noarchive` for staging; production assembly removes that tag
and publishes the crawlable production robots policy. Staging remains noindexed.


## Final-domain migration

Final public production origin: `https://drfarahvipurgentcare.com`  
Final staging origin: `https://staging.drfarahvipurgentcare.com`

`booking.js` and `registration.js` recognize both final and temporary
origins during the cutover window. Staging remains `noindex` with
`robots.txt: Disallow: /`. Production is assembled by Jenkins using the
production robots/Apache policy. The operator accepted an initial targeted
legacy redirect set for launch while GoDaddy hosting remains available as the
recovery source and the complete URL inventory is finished after launch.

See `docs/migration/FINAL_DOMAIN_CUTOVER.md`.
