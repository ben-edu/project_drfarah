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
Times shown in America/Los_Angeles. Contact form has no backend yet; it
validates and directs urgent matters to the phone.

## Extensionless URLs
Links use /services etc. Verified working on staging: nginx proxies extensionless
requests to Apache, which honors the shipped .htaccess (AllowOverride All).
Keep .htaccess.

## Assets
The frontend now includes approved Dr. Farah/clinic imagery plus a temporary
runtime reconstruction workaround for several critical hero/physician images.
Do not reintroduce retired generic AI placeholders. The Services hero is a known
visual-quality backlog item (too soft/blurred) and should be corrected in a
focused visual change.

The legacy WordPress insurer-image hotlinks were removed before production.
The launch version uses the accessible named insurance text cards already in
the HTML. Approved local artwork can replace them later without adding a
runtime dependency on the old host.

## Legal / noindex
Legal pages are drafts pending clinic + counsel review. All pages carry
noindex,nofollow,noarchive and robots.txt disallows all (temporary staging domain).
Remove at final-domain migration (1E).


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
