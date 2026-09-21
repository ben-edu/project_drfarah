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

The API deployment contains a `:prod` image placeholder for both the migration
init container and API container. Jenkins `main` renders both to the exact
40-character Git SHA before applying the Deployment.

## Required out-of-band secrets

Before production promotion, namespace `drfarah` must contain:

- `harbor-regcred`
- `drfarah-db-secret`
- `drfarah-api-secret`

Real secret values must never be committed.

## Fail-closed production blockers

`configmap.yaml` intentionally contains `REPLACE_BEFORE_PRODUCTION` for
unconfirmed production SMTP non-secret values. Jenkins `main` refuses to
deploy production while those markers remain.

The frontend production deployment also refuses to run while
`frontend/.htaccess.production` contains `CUTOVER_BLOCKER`, which represents
the incomplete legacy WordPress redirect inventory.

Do not remove either blocker until its prerequisite is genuinely complete.

## Deployment

- feature/chore branches: validation only;
- `dev`: staging deploy;
- `main`: production deploy after explicit approval.

Full cutover procedure:
`docs/migration/FINAL_DOMAIN_CUTOVER.md`.


## Production data-protection gate

**BACKUP_READINESS_BLOCKER**

Do not remove this marker until a production PostgreSQL backup destination,
retention policy, restore procedure, and at least one restore test are
documented and verified. Production stores appointment and patient-registration
data; a green application deployment is not sufficient evidence of data
recoverability.
