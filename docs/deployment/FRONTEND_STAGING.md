# Frontend Staging Deployment

## Branch-to-environment mapping

| Branch | Environment | Deploy frontend? |
|---|---|---|
| `feature/*` | None (validation only) | No |
| `dev` | Staging | Yes, via Jenkins |
| `main` | Production | Not yet configured |

## Staging target

| Setting | Value |
|---|---|
| Host | `staging.drfarah.proxbenovh.cloud` |
| Hestia server | `192.168.100.75:2275` |
| SSH user | `benweb` |
| Docroot | `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html` |
| Jenkins credential | `hestia-benweb-ssh` |

## Deployment mechanism

Deployment occurs through the Jenkins `Frontend — deploy staging` stage, which
runs exclusively on the `dev` branch.

1. **Preflight** — SSH to Hestia as `benweb`, verify docroot exists and is
   writable, create and delete a temporary test file.
2. **rsync** — `rsync -av --delete --exclude='.env' --exclude='.well-known'`
   from `frontend/` to the staging docroot.
3. **Smoke test** — verify HTTP 200 for `/`, `/styles.css`, `/app.js`,
   `/robots.txt`, and confirm content markers (Dr. Farah title, noindex meta,
   robots Disallow rule).

## Preflight checks (performed each deploy)

- Docroot exists at the expected path.
- Connected user is `benweb`.
- Write access confirmed via temporary file create/delete.
- Failure produces a clear error message without exposing credentials.

## Smoke tests (performed each deploy)

- `GET /` returns 200 and contains `Dr. Farah` marker and
  `noindex,nofollow,noarchive` meta tag.
- `GET /styles.css` returns 200.
- `GET /app.js` returns 200.
- `GET /robots.txt` returns 200 and contains `Disallow: /`.
- TLS verification remains successful.
- Retries with short delays (5 attempts, 3-second intervals) to accommodate
  HAProxy/Hestia serving latency.

## Rollback procedure

1. Identify the last known-good commit on `dev`.
2. Run the Jenkins dev build from that commit (or revert and push).
3. Jenkins will rsync the previous frontend content to the staging docroot.
4. Do not manually restore files outside Jenkins.

## No-index status

Temporary-domain indexing protection is active:
- `<meta name="robots" content="noindex,nofollow,noarchive">` in `index.html`
- `robots.txt`: `Disallow: /`

Both must be removed or changed during final-domain migration.

## Production deployment

Production frontend deployment (`main` -> `drfarah.proxbenovh.cloud`) is
**not configured**. The `main` branch runs validation and API stages only.
A separate step will add the production deployment stage after the staging
frontend is reviewed and accepted.

## Exclusions

- `.env` — excluded from rsync (never present in `frontend/` but protected)
- `.well-known` — excluded from rsync (preserved for Let's Encrypt / Hestia)

## Constraints

- No `sudo`, `root`, `chmod`, `chown`, or group permission workarounds.
- No manual file copies to Hestia.
- No HAProxy, DNS, TLS, or Hestia domain configuration changes.
- No API, PostgreSQL, Keycloak, admin panel, or Kubernetes deployment.
- No credentials committed or exposed.
