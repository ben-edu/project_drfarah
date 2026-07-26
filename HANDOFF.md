# HANDOFF — 2026-07-26 (Step 04B)

## Current state

- **Branch:** `feature/frontend-staging-deploy`
- **Base:** `dev` (Step 04A frontend prototype merged via PR #4).
- **Commit:** see `SESSION_LOG.md` for the commit SHA after push.

## Work completed (Step 04B — Deploy Approved Frontend to Staging)

### Preflight (read-only)
- DNS: `staging.drfarah.proxbenovh.cloud` resolves to `87.98.174.211`.
- TLS: valid Let's Encrypt certificate, SAN covers the staging hostname.
- HTTPS: HTTP 200 (default Hestia placeholder page).
- Docroot: `/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html`
  exists, owned by `benweb:www-data`.
- Write access: `benweb` can create/delete files in docroot (verified).
- Current content: default placeholder files only (no prior frontend deploy).
- benweb shell: `/bin/bash` (SSH-ready when key is in place).

### Jenkinsfile changes
- Added `Frontend — deploy staging` stage:
  - **Trigger:** `dev` branch only. Never runs on `feature/*` or `main`.
  - **Credential:** `hestia-benweb-ssh` (SSH user private key).
  - **Preflight:** SSH to Hestia as `benweb`, confirm docroot exists and
    is writable via temporary file create/delete.
  - **Deploy:** `rsync -av --delete --exclude='.env' --exclude='.well-known'`
    from `frontend/` to staging docroot.
  - **Smoke test:** HTTP 200 retry loop (5 attempts, 3s interval) for `/`,
    `/styles.css`, `/app.js`, `/robots.txt`.
  - **Content verification:** grep for `Dr. Farah` marker, noindex meta,
    `Disallow: /` in robots.txt.
  - No sudo, chmod, chown, root, manual copy, or Hestia rebuild.
- Updated header comments to reflect deployment capability.
- All existing stages preserved unchanged.

### Documentation created/updated
- Created: `docs/deployment/FRONTEND_STAGING.md` — full deployment
  documentation including branch mapping, mechanism, preflight, smoke tests,
  rollback procedure, no-index status, constraints.
- Updated: `docs/architecture/README.md` — added deployment section link.
- Updated: `frontend/README.md` — added deployment section.
- Updated: `HANDOFF.md` — this file.
- Updated: `SESSION_LOG.md` — session record appended.

### What was NOT done (intentionally)

- No frontend file changes (index.html, styles.css, app.js, robots.txt are
  identical to Step 04A).
- No deployment from feature branches (validation only).
- No production deployment (main deploys nothing).
- No API, PostgreSQL, Keycloak, admin panel, or Kubernetes deployment.
- No HAProxy, DNS, TLS, or Hestia configuration changes.
- No manual file copies to Hestia.
- No credentials committed or exposed.
- No PR merge (awaiting operator review).

## Deployment behavior summary

| Branch | Validation | Deploy to staging |
|---|---|---|
| `feature/*` | Yes | No |
| `dev` | Yes | Yes (Hestia rsync) |
| `main` | Yes | No (production not configured) |

## Files the next session must read first

1. `HANDOFF.md` — this file.
2. `SESSION_LOG.md` — latest session entry.
3. `docs/deployment/FRONTEND_STAGING.md` — staging deployment details.
4. `frontend/README.md` — placeholder list and deployment notes.
5. `PROJECT.md` — product brief (for context on next steps).

## Post-merge — what the operator must inspect

After the PR is merged into `dev`, Jenkins will automatically build `dev`
and trigger the `Frontend — deploy staging` stage. The operator must:

1. Open the Jenkins dev build console and confirm the
   `Frontend — deploy staging` stage completed successfully.
2. Verify `https://staging.drfarah.proxbenovh.cloud/` shows the Dr. Farah
   prototype (not the Hestia default page).
3. Confirm all four assets return HTTP 200:
   - `https://staging.drfarah.proxbenovh.cloud/`
   - `https://staging.drfarah.proxbenovh.cloud/styles.css`
   - `https://staging.drfarah.proxbenovh.cloud/app.js`
   - `https://staging.drfarah.proxbenovh.cloud/robots.txt`
4. Confirm noindex meta and robots Disallow rule are present.
5. Open the booking modal and verify it functions (frontend-only).

## Recommended next step

**Visually review the deployed staging frontend** at
`https://staging.drfarah.proxbenovh.cloud/` before any API integration or
backend deployment. Do not start Step 03B (staging deployment and database
provisioning) until the design is reviewed and accepted.
