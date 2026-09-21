# Kubernetes — Dr. Farah production

Production namespace and manifests for the final clinic domain.

## Final production endpoints

- frontend: `https://drfarahvipurgentcare.com`
- API: `https://api.drfarahvipurgentcare.com`
- admin: `https://admin.drfarahvipurgentcare.com`
- Keycloak issuer remains `https://keycloak.soria-academie.fr/realms/drfarah`

## Environment isolation

Production namespace: `drfarah`  
Staging namespace: `drfarah-staging`

Production has independent:
- PostgreSQL StatefulSet/PVC;
- database credentials;
- API secret;
- Deployment and Service;
- Traefik Ingress;
- Hestia frontend/admin docroots.

Never reuse staging database credentials in production.

## Production resources

- `namespace.yaml`
- `postgres-statefulset.yaml`
- `postgres-service.yaml`
- `configmap.yaml`
- `secret.example.yaml`
- `api-deployment.yaml`
- `api-service.yaml`
- `api-ingress.yaml`
- `postgres-backup-cronjob.yaml`
- `backup/Dockerfile`
- `backup/backup.sh`

The API deployment contains a `:prod` image placeholder for both the migration
init container and API container. Jenkins `main` renders both to the exact
40-character Git SHA before applying the Deployment.

## Production secrets

The production deployment requires:

- `harbor-regcred`
- `drfarah-db-secret`
- `drfarah-api-secret`

When both DB/API secrets are absent, Jenkins runs
`scripts/bootstrap-production-secrets.sh` once: it generates an independent
production DB password and copies only the approved Soria SMTP and Harbor
credentials from staging without printing values. Existing DB/API secrets are
preserved and validated. A partial state fails closed.

Jenkins also creates/updates `drfarah-backup-ssh` from its existing
`hestia-benweb-ssh` credential plus a freshly scanned Hestia host key. Replace
this with a dedicated restricted backup key after the immediate cutover.

Real secret values must never be committed.

## Approved temporary launch decisions

The operator explicitly approved the Soria SMTP relay as the temporary
production email service. Non-secret host/from/to values are in
`configmap.yaml`; credentials stay in `drfarah-api-secret`.

The operator also accepted launching with the confirmed high-value legacy
redirects while the complete WordPress URL inventory is finished after launch.
GoDaddy hosting is retained as the recovery source and must not be deleted
during stabilization. `frontend/.htaccess.production` records this decision as
`LEGACY_REDIRECT_RISK_ACCEPTED: 2026-09-21`.

## Deployment

- feature/chore branches: validation only;
- `dev`: staging deploy;
- `main`: production deploy after explicit approval.

Full cutover procedure:
`docs/migration/FINAL_DOMAIN_CUTOVER.md`.


## Production PostgreSQL backup and restore

Production backup is part of the `main` deployment and fails closed before the
public frontend/admin are published:

- `drfarah-postgres-backup` runs daily at `09:17 UTC`;
- `pg_dump --format=custom` creates a logical backup;
- the backup is copied over SSH to the independent Hestia host at
  `/home/benweb/backups/drfarah-postgres`;
- the destination directory is mode `0700` and archives are mode `0600`;
- archives older than 30 days are deleted from that exact directory;
- every production deployment starts an immediate backup Job, downloads that
  exact off-cluster archive, and restores it into a disposable PostgreSQL 16
  container;
- frontend/admin publication proceeds only when the restore test finds the
  restored public schema.

Manual restore outline:

```bash
docker run -d --name drfarah-restore \
  -e POSTGRES_USER=restore \
  -e POSTGRES_PASSWORD='<temporary-password>' \
  -e POSTGRES_DB=restore \
  postgres:16-alpine

docker cp drfarah-YYYYMMDDTHHMMSSZ-POD.dump drfarah-restore:/backup.dump
docker exec drfarah-restore \
  pg_restore --no-owner --no-privileges \
  -U restore -d restore /backup.dump
```

Never restore over the live production database. Use a disposable database or
container, validate it, and follow a separately approved recovery window for an
actual incident.
