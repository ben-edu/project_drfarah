#!/bin/sh

# One-time production secret bootstrap. Run from a trusted Kubernetes
# management shell. Values are generated/copied in memory and never printed.
# This script deliberately refuses to overwrite initialized production secrets.

# Keep secret material out of logs even if a caller invokes this script from a
# traced shell (for example Jenkins' default `sh -x` wrapper).
set +x
set -eu
umask 077

production_namespace='drfarah'
staging_namespace='drfarah-staging'
database_user='drfarah'
database_name='drfarah'

for command_name in kubectl openssl base64 mktemp; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "FAIL: required command is missing: $command_name" >&2
    exit 1
  }
done

if ! kubectl get namespace "$production_namespace" >/dev/null 2>&1; then
  kubectl create namespace "$production_namespace"
fi

for existing_secret in drfarah-db-secret drfarah-api-secret; do
  if kubectl -n "$production_namespace" \
    get secret "$existing_secret" >/dev/null 2>&1; then
    echo "FAIL: secret/$existing_secret already exists; refusing to overwrite it." >&2
    echo "Inspect the existing production state instead of rotating blindly." >&2
    exit 1
  fi
done

if kubectl -n "$production_namespace" \
  get pvc data-drfarah-postgres-0 >/dev/null 2>&1; then
  echo "FAIL: a production PostgreSQL PVC already exists without managed secrets." >&2
  echo "Recover the original credentials; do not generate replacements." >&2
  exit 1
fi

for staging_secret in \
  harbor-regcred \
  drfarah-staging-api-secret \
  drfarah-staging-db-secret; do
  kubectl -n "$staging_namespace" \
    get secret "$staging_secret" >/dev/null || {
      echo "FAIL: staging source secret is missing: $staging_secret" >&2
      exit 1
    }
done

smtp_user_encoded="$(
  kubectl -n "$staging_namespace" \
    get secret drfarah-staging-api-secret \
    -o jsonpath='{.data.SMTP_USER}'
)"
smtp_password_encoded="$(
  kubectl -n "$staging_namespace" \
    get secret drfarah-staging-api-secret \
    -o jsonpath='{.data.SMTP_PASSWORD}'
)"
staging_db_password_encoded="$(
  kubectl -n "$staging_namespace" \
    get secret drfarah-staging-db-secret \
    -o jsonpath='{.data.POSTGRES_PASSWORD}'
)"
harbor_config_encoded="$(
  kubectl -n "$staging_namespace" \
    get secret harbor-regcred \
    -o jsonpath='{.data.\.dockerconfigjson}'
)"

for encoded_value in \
  "$smtp_user_encoded" \
  "$smtp_password_encoded" \
  "$staging_db_password_encoded" \
  "$harbor_config_encoded"; do
  [ -n "$encoded_value" ] || {
    echo "FAIL: a required staging secret key is empty." >&2
    exit 1
  }
done

smtp_user="$(printf '%s' "$smtp_user_encoded" | base64 -d)"
smtp_password="$(printf '%s' "$smtp_password_encoded" | base64 -d)"
production_db_password="$(openssl rand -hex 32)"
production_database_url="postgresql+psycopg://${database_user}:${production_db_password}@drfarah-postgres:5432/${database_name}"

if [ "$(printf '%s' "$production_db_password" | base64 | tr -d '\n')" = "$staging_db_password_encoded" ]; then
  echo "FAIL: generated production DB password unexpectedly matches staging." >&2
  exit 1
fi

database_manifest="$(mktemp)"
api_manifest="$(mktemp)"
harbor_manifest="$(mktemp)"
harbor_config="$(mktemp)"

cleanup() {
  rm -f \
    "$database_manifest" \
    "$api_manifest" \
    "$harbor_manifest" \
    "$harbor_config"
  unset \
    smtp_user_encoded \
    smtp_password_encoded \
    staging_db_password_encoded \
    harbor_config_encoded \
    smtp_user \
    smtp_password \
    production_db_password \
    production_database_url
}
trap cleanup EXIT HUP INT TERM

printf '%s' "$harbor_config_encoded" | base64 -d > "$harbor_config"

kubectl -n "$production_namespace" \
  create secret generic drfarah-db-secret \
  --from-literal=POSTGRES_USER="$database_user" \
  --from-literal=POSTGRES_PASSWORD="$production_db_password" \
  --from-literal=POSTGRES_DB="$database_name" \
  --dry-run=client \
  -o yaml \
  > "$database_manifest"

kubectl -n "$production_namespace" \
  create secret generic drfarah-api-secret \
  --from-literal=DATABASE_URL="$production_database_url" \
  --from-literal=POSTGRES_USER="$database_user" \
  --from-literal=POSTGRES_PASSWORD="$production_db_password" \
  --from-literal=SMTP_USER="$smtp_user" \
  --from-literal=SMTP_PASSWORD="$smtp_password" \
  --dry-run=client \
  -o yaml \
  > "$api_manifest"

kubectl -n "$production_namespace" \
  create secret generic harbor-regcred \
  --type=kubernetes.io/dockerconfigjson \
  --from-file=.dockerconfigjson="$harbor_config" \
  --dry-run=client \
  -o yaml \
  > "$harbor_manifest"

kubectl apply \
  -f "$database_manifest" \
  -f "$api_manifest" \
  -f "$harbor_manifest"

cleanup
trap - EXIT HUP INT TERM

echo "Production namespace and three required secrets are ready."
echo "No secret values were printed."
