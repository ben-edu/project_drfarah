# Frontend Staging Deployment

> Updated for the final clinic-domain migration. Do not merge the cutover branch
> until the new staging Hestia domains, HAProxy routes, TLS and Keycloak staging
> admin origin are ready.

## Branch mapping

| Branch | Environment | Deployment |
|---|---|---|
| feature/fix/chore | validation only | no deployment |
| `dev` | final staging | Jenkins deploys |
| `main` | production | Jenkins deploys only after production gates are cleared |

## Final staging targets

| Component | Host / target |
|---|---|
| Public frontend | `staging.drfarahvipurgentcare.com` |
| Frontend docroot | `/home/benweb/web/staging.drfarahvipurgentcare.com/public_html` |
| API | `api.staging.drfarahvipurgentcare.com` |
| Admin SPA | `admin.staging.drfarahvipurgentcare.com` |
| Admin docroot | `/home/benweb/web/admin.staging.drfarahvipurgentcare.com/public_html` |
| API namespace | `drfarah-staging` |
| Hestia server | `192.168.100.75:2275` |
| SSH user / Jenkins credential | `benweb` / `hestia-benweb-ssh` |

The old temporary staging/admin/API hosts remain compatibility routes during the
migration window but are no longer the target environment after the cutover
branch reaches `dev`.

## Delivery mechanism

Jenkins is authoritative for deployment.

For `dev`:
1. validate repository, Python tests, PostgreSQL tests, Docker image and static assets;
2. build/push the immutable API image plus `:dev`;
3. apply staging Kubernetes resources and run the migration init container;
4. run staging API smoke checks;
5. rsync `frontend/` to the final staging frontend docroot as `benweb`;
6. rsync `admin/` to the final staging admin docroot as `benweb`;
7. run HTTPS smoke checks.

The staging frontend keeps the repository `.htaccess`, noindex metadata and
`robots.txt: Disallow: /`. Production-only files
`.htaccess.production` and `robots.production.txt` are excluded from the
staging rsync.

## Production separation

Production is not the staging docroot with different DNS. It uses:
- frontend `drfarahvipurgentcare.com`;
- admin `admin.drfarahvipurgentcare.com`;
- API `api.drfarahvipurgentcare.com`;
- Kubernetes namespace `drfarah`;
- independent PostgreSQL secrets/PVC;
- production-only crawlable robots and Apache redirect rules.

See `docs/migration/FINAL_DOMAIN_CUTOVER.md` for DNS, HAProxy, TLS, Keycloak,
legacy WordPress redirects, insurer assets, backup requirements and promotion
sequence.

## Rollback

Do not hand-edit deployed files as the normal rollback. Revert the bad change on
`dev`, validate staging, and redeploy through Jenkins. For the production
domain cutover itself, retain the old WordPress hosting/DNS target during the
stabilization window so apex DNS can be restored if required.
