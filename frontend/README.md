# Frontend — Dr. Farah VIP Urgent Care

Public website prototype for `drfarah.proxbenovh.cloud` and
`staging.drfarah.proxbenovh.cloud`.

## Source

The design prototype was created by the design owner and supplied as
`project-sources/drfarah_design_prototype_v1.zip`. Claude Code integrated the
approved prototype faithfully — no redesign, restyle, or framework migration
was performed.

## Structure

```
frontend/
├── index.html      Public homepage with integrated booking modal
├── styles.css      Complete responsive stylesheet
├── app.js           Booking modal interaction (frontend-only)
├── robots.txt       Disallow all (temporary-domain protection)
└── README.md
```

## Status

- **Design:** approved prototype v1, integrated without reinterpretation.
- **Booking:** frontend-only modal with four steps, service preselection,
  review, and prototype success state. No network requests, no API connection,
  no data storage.
- **Backend independence:** the frontend is fully static and does not depend
  on the FastAPI backend or any runtime service.
- **No-index protection:** active via `<meta name="robots">` and
  `robots.txt`. Must be removed or changed during final-domain migration.
- **Direct `/book` route:** not yet implemented. Belongs to a later step.

## Unresolved placeholders

The following prototype values must be replaced with verified clinic
information before the site is promoted as final production content:

| Placeholder | Location |
|---|---|
| Phone number `(310) 000-0000` / `+13100000000` | Header, hero, location, footer, mobile bar |
| Email `contact@example.com` | Location, footer |
| Exact clinic address | Location section map card |
| Office hours | Not yet present in prototype |
| Legal text (privacy policy, notice of privacy practices, accessibility) | Footer links (all `#`) |
| Real portrait photograph | About section (CSS artwork placeholder) |
| Clinic photography | Not yet present |
| Appointment availability (dates/times) | Booking step 2 |
| Verified patient reviews | Not yet present |
| Final service list and descriptions | Service cards |
| Credentials wording | About section |
| Logo / brand mark | Header and footer (text-based `DF` mark) |

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
- Google Fonts loaded from `fonts.googleapis.com`. Self-hosting or privacy
  review is a later production decision (documented, not changed in this step).
- No patient data logged to console or stored.

## Booking behavior (current step)

- All booking entry points open the same four-step modal.
- Service preselection is preserved from the entry context.
- Four-step navigation with progress indicator, back button, and review step.
- Success state shows a prototype notice (no real booking created).
- No network requests, no localStorage/sessionStorage, no API connection.
- The `/book` route and API integration belong to later steps.

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
