#!/bin/sh

# Sync the Jenkins-managed Google service-account JSON into one or more
# Kubernetes namespaces without printing or committing credential material.
#
# Required environment:
#   GOOGLE_DATA_MANAGER_CREDENTIALS_FILE=/path/to/jenkins-secret-file
#
# Usage:
#   sh scripts/sync-google-data-manager-credentials.sh drfarah-staging drfarah

# Jenkins may invoke shell steps with tracing enabled. Disable it before any
# credential handling so file paths/content cannot be echoed accidentally.
set +x
set -eu
umask 077

credential_file="${GOOGLE_DATA_MANAGER_CREDENTIALS_FILE:-}"
secret_name='drfarah-google-data-manager-credentials'
secret_key='credentials.json'

if [ "$#" -lt 1 ]; then
  echo "FAIL: provide at least one Kubernetes namespace." >&2
  exit 1
fi

if [ -z "$credential_file" ]; then
  echo "FAIL: GOOGLE_DATA_MANAGER_CREDENTIALS_FILE is not set." >&2
  exit 1
fi

if [ ! -r "$credential_file" ]; then
  echo "FAIL: Google Data Manager credential file is missing or unreadable." >&2
  exit 1
fi

for command_name in kubectl python3 mktemp; do
  command -v "$command_name" >/dev/null 2>&1 || {
    echo "FAIL: required command is missing: $command_name" >&2
    exit 1
  }
done

# Validate only the credential shape. Never print field values.
python3 - "$credential_file" <<'PY'
import json
import sys

path = sys.argv[1]
with open(path, "r", encoding="utf-8") as handle:
    payload = json.load(handle)

if payload.get("type") != "service_account":
    raise SystemExit("FAIL: credential JSON is not a service_account credential")

for key in ("project_id", "private_key", "client_email", "token_uri"):
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        raise SystemExit(f"FAIL: credential JSON is missing required field: {key}")
PY

manifest="$(mktemp)"
cleanup() {
  rm -f "$manifest"
}
trap cleanup EXIT HUP INT TERM

for namespace in "$@"; do
  kubectl get namespace "$namespace" >/dev/null 2>&1 || {
    echo "FAIL: Kubernetes namespace does not exist: $namespace" >&2
    exit 1
  }

  : > "$manifest"

  kubectl -n "$namespace" \
    create secret generic "$secret_name" \
    --from-file="${secret_key}=${credential_file}" \
    --dry-run=client \
    -o yaml \
    > "$manifest"

  kubectl apply -f "$manifest" >/dev/null

  key_present="$(
    kubectl -n "$namespace" \
      get secret "$secret_name" \
      -o 'jsonpath={.data.credentials\.json}' \
      2>/dev/null \
      || true
  )"

  if [ -z "$key_present" ]; then
    echo "FAIL: secret/$secret_name is missing $secret_key in namespace $namespace" >&2
    exit 1
  fi

  unset key_present
  echo "OK: secret/$secret_name synchronized in namespace $namespace"
done

cleanup
trap - EXIT HUP INT TERM
