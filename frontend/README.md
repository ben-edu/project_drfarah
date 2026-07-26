# Frontend — Dr. Farah VIP Urgent Care

Public website prototype for `drfarah.proxbenovh.cloud` and
`staging.drfarah.proxbenovh.cloud`.

## Source

The design prototype was created by the design owner and supplied as
`project-sources/drfarah_design_prototype_v2.zip`. Claude Code integrated the
approved prototype faithfully — no redesign, restyle, or framework migration
was performed.

## Structure

```
frontend/
├── index.html      Public homepage with integrated booking modal
├── styles.css      Complete responsive stylesheet
├── app.js           Booking modal interaction (frontend-only)
├── robots.txt       Disallow all (temporary-domain protection)
├── assets/          SVG visual assets (logos, icons, illustrations)
│   ├── favicon.svg
│   ├── logo-mark.svg
│   ├── doctor-portrait.svg
│   ├── hero-clinic.svg
│   ├── urgent-care.svg
│   ├── mobile-care.svg
│   ├── traveler-care.svg
│   ├── rejuvenation-main.svg
│   ├── clinic-map.svg
│   └── og-preview.svg
└── README.md
```

## Status

- **Design:** approved prototype v2, integrated without reinterpretation.
- **Booking:** four-step modal with real API integration. Services loaded
  dynamically from `GET /api/v1/services`. Slots loaded from
  `GET /api/v1/availability`. Appointments submitted to
  `POST /api/v1/appointments` with conflict detection (409 handling).
  Date picker with 14-day rolling window. Slot grid with show-more toggle.
  Loading and error states for all network operations.
- **Backend independence:** the frontend is fully static and does not depend
  on the FastAPI backend or any runtime service.
- **No-index protection:** active via `<meta name="robots">` and
  `robots.txt`. Must be removed or changed during final-domain migration.
- **Logo/favicon:** SVG favicon and logo mark in `assets/`. Linked via
  `<link rel="icon">` and used in header/footer branding.
- **Cookie notice:** fixed-position banner at bottom of viewport. Uses
  `localStorage` key `drfarah-cookie-notice` to remember dismissal. No
  third-party cookies, no analytics, no tracking scripts.
- **SEO:** Open Graph tags, Twitter card, canonical URL, MedicalClinic
  structured data, and `noindex,nofollow,noarchive` meta tag for temporary
  staging protection.
- **Richer slot UI:** booking step 2 presents 16 time slots (8 visible by
  default) with a "Show more slots" button that reveals the full set.
- **Direct `/book` route:** not yet implemented. Belongs to a later step.

## Temporary placeholder values

The following prototype values must be replaced with verified clinic
information before the site is promoted as final production content:

| Placeholder | Location |
|---|---|
| Phone number `(310) 555-0189` / `+13105550189` | Utility bar, header, hero, location, footer, mobile bar |
| Email `appointments@drfarah.proxbenovh.cloud` | Utility bar, location, footer |
| Exact clinic address `9400 Brighton Way, Beverly Hills, CA 90210` | Location section map card |
| Office hours `Daily by appointment` | Location section |
| Legal text (privacy policy, notice of privacy practices, accessibility) | Footer links (all `#`) |
| Real portrait photograph | About section (SVG illustration placeholder) |
| Clinic photography | Hero, service cards (SVG illustration placeholders) |
| Appointment availability (dates/times) | Booking step 2 (prototype demo data) |
| Verified patient reviews | Not yet present |
| Final service list and descriptions | Service cards |
| Credentials wording | About section |
| Domain (canonical URL, email domain) | Meta tags, email addresses |

The temporary site must not be promoted as final production content until all
placeholders are verified and replaced.

## Temporary-domain indexing protection

The temporary domains (`drfarah.proxbenovh.cloud`,
`staging.drfarah.proxbenovh.cloud`) are not the clinic's final public domain.

- `robots.txt`: `Disallow: /`
- `<meta name="robots" content="noindex,nofollow,noarchive">` in `index.html`

Both must be removed or changed to the production rules during final-domain
migration. Do not create a sitemap until the final domain is active.

## Privacy notes

- No analytics or tracking scripts.
- No third-party cookies.
- Cookie notice uses `localStorage` only (key: `drfarah-cookie-notice`).
- Google Fonts loaded from `fonts.googleapis.com`. Self-hosting or privacy
  review is a later production decision (documented, not changed in this step).
- No patient data logged to console or stored.

## Booking behavior

- All booking entry points open the same four-step modal.
- Service preselection is preserved from the entry context.
- Step 1: service choices loaded dynamically from `GET /api/v1/services`.
- Step 2: date picker (14-day rolling window) + slot grid loaded from
  `GET /api/v1/availability`. Slots shown 8 at a time with "Show more
  slots" toggle.
- Step 3: patient contact form (name, email, phone, reason).
- Step 4: review and submit.
- On submit, the form POSTs to
  `POST /api/v1/appointments` with the selected service and slot.
- On 201: booking reference ID and confirmation details are shown.
- On 409: "This slot was just taken" message with suggestion to pick another.
- On other errors: error message with clinic phone number for fallback.
- Duplicate submission prevention: submit button disabled during request.
- Legacy `POST /api/v1/bookings` endpoint preserved but no longer used by
  the frontend.

## Deployment

Staging deployment is configured in the Jenkinsfile (`Frontend — deploy
staging` stage). See `docs/deployment/FRONTEND_STAGING.md` for full details.

| Aspect | Detail |
|---|---|
| Target | `staging.drfarah.proxbenovh.cloud` |
| Mechanism | `rsync` from `frontend/` to Hestia docroot via `benweb` SSH |
| Trigger | Jenkins build on `dev` only |
| Credential | `hestia-benweb-ssh` |
| Exclusions | `.env`, `.well-known` |
| Rollback | Redeploy previous known-good commit through Jenkins |

## Next step

Visually review the deployed staging frontend at
`https://staging.drfarah.proxbenovh.cloud/` before any API integration or
backend deployment. Do not start the `/book` route or connect the booking
form to the API until the design is reviewed.
