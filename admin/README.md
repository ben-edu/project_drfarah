# Dr. Farah — Admin SPA

Internal admin single-page application for staff management of the Dr. Farah
platform.  Static HTML/CSS/JS — no build step, no framework.

## Architecture

- `index.html` — shell (dark warm-noir theme, Cormorant + Inter).
- `app.js` — Keycloak Authorization Code + PKCE S256 flow, fetches identity
  from `GET /api/v1/admin/me` and renders it.
- `config.js` — runtime configuration (Keycloak URL, realm, client ID, API
  base).  All values are public.  Change `API_BASE` per environment without
  touching `app.js`.
- `styles.css` — brand-aligned styling.

## Authentication flow

1. User clicks **Sign in with Keycloak**.
2. Keycloak-js (loaded from CDN, pinned version) performs Authorization Code
   + PKCE S256 against the `drfarah-admin` public client.
3. On success the SPA calls `GET /api/v1/admin/me` with the Bearer token.
4. Identity (username, email, roles) is displayed in the panel.
5. `keycloak.updateToken(30)` is called before every API request to ensure
   the token is fresh.
6. Tokens are held **in memory only** (keycloak-js manages this).  Nothing
   is written to `localStorage` or `sessionStorage`.

## Serving the app

The SPA **must** be served over a URL registered in the Keycloak client:

- **Valid Redirect URIs:** `https://admin.staging.drfarahvipurgentcare.com/*`
- **Web Origins:** `https://admin.staging.drfarahvipurgentcare.com`

### Local testing

To test locally you must either:

**Option A** — Add a localhost redirect URI + web origin to the Keycloak
client `drfarah-admin` (e.g. `http://localhost:8080/*` and
`http://localhost:8080`), then serve the `admin/` directory:

    python3 -m http.server 8080 --directory admin

**Option B** — Deploy the `admin/` directory to the admin host
(`admin.drfarah.proxbenovh.cloud`) and test against the live URL.

### Production / staging

The admin SPA is deployed to `admin.drfarah.proxbenovh.cloud` (Hestia).
`config.js` points `API_BASE` to the appropriate API host.

## Configuration

| Key | Value | Notes |
|---|---|---|
| `KEYCLOAK_URL` | `https://keycloak.soria-academie.fr` | Keycloak base URL |
| `REALM` | `drfarah` | Keycloak realm |
| `CLIENT_ID` | `drfarah-admin` | Public OIDC client (PKCE) |
| `API_BASE` | `https://api.staging.drfarahvipurgentcare.com/api/v1` | API base URL |

No secrets — this is a public OIDC client.


## Patient registrations

Authenticated users with the `clinic-staff` realm role can also review online patient registrations:

- `GET /api/v1/admin/registrations` — filter/search the registration queue.
- `GET /api/v1/admin/registrations/{id}` — view registration detail.

The admin API never exposes the public resume-token hash. The current admin view is read-only for registration data; editing clinical intake is intentionally outside this phase.


## Final-domain Keycloak migration

Keycloak remains at `https://keycloak.soria-academie.fr`, realm `drfarah`,
client `drfarah-admin`.

Final explicit client settings must include:

- Redirect/post-logout: `https://admin.staging.drfarahvipurgentcare.com/*`
- Redirect/post-logout: `https://admin.drfarahvipurgentcare.com/*`
- Web origin: `https://admin.staging.drfarahvipurgentcare.com`
- Web origin: `https://admin.drfarahvipurgentcare.com`

The old temporary admin origin may remain only during the transition window.
