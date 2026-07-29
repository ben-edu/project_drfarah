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
assets/*.jpg are temporary AI-generated placeholders. Replace with real approved
clinic photography before production; keep the same filenames.

## Legal / noindex
Legal pages are drafts pending clinic + counsel review. All pages carry
noindex,nofollow,noarchive and robots.txt disallows all (temporary staging domain).
Remove at final-domain migration (1E).
