# Dr. Farah — Frontend (Phase 1)

Static, build-free frontend for the Dr. Farah VIP Urgent Care site. Plain HTML +
CSS + vanilla JS, deployed to Hestia via Jenkins (rsync). No build step.

## Pages
- `index.html` — home (hero, care paths, doctor, how-it-works, visit modes, reviews, book CTA)
- `services.html` — services (`/services`)
- `about.html` — about Dr. Farah (`/about`)
- `contact.html` — contact + general enquiry form (`/contact`)
- `book.html` — multi-step booking wizard wired to the API (`/book`)
- `privacy.html`, `terms.html`, `accessibility.html`, `notice-of-privacy-practices.html` — legal (placeholders pending legal review)
- `404.html` — not found

## API wiring (book.html + booking.js)
`booking.js` derives `API_BASE` from the hostname:
- `staging.drfarah.proxbenovh.cloud` → `https://api.staging.drfarah.proxbenovh.cloud/api/v1`
- `drfarah.proxbenovh.cloud` / `www.` → `https://api.drfarah.proxbenovh.cloud/api/v1`
- fallback → staging API

Endpoints used: `GET /services`, `GET /availability`, `POST /appointments`
(handles 201 / 409 slot-taken / 422). All times shown in `America/Los_Angeles`.

The contact form has no backend endpoint yet (ContactRequest API is future work);
it validates client-side and directs urgent matters to the phone.

## Extensionless URLs
Links use `/services` (no `.html`). `.htaccess` rewrites extensionless URLs to
`<name>.html` and sets the 404 document. **If Hestia serves via nginx rather than
Apache**, this rewrite must be added to the nginx template instead — see the
deploy notes. Alternatively the pages resolve directly at `/services.html`.

## Assets
`assets/*.jpg` are temporary AI-generated placeholders (compressed). Replace with
real approved clinic photography before production; keep the same filenames.

## Legal / content status
Address, phone, credentials, services, and pricing are drawn from the current
public site and PROJECT.md and are marked "pending verification". Legal pages are
drafts for review by the clinic and counsel. Regenerative/rejuvenation wording is
consultation-framed and must be medically/legally reviewed before public launch.

## Noindex
All pages carry `noindex,nofollow,noarchive` and `robots.txt` disallows all —
correct for the temporary staging domain. Remove at final-domain migration (1E).
