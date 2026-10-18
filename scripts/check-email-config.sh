#!/bin/sh
# Fail deployment before replacing a working API if transactional email cannot
# be configured. Never print Secret data (including encoded values).
set +x
set -eu

if [ "$#" -ne 3 ]; then
  echo "Usage: check-email-config.sh NAMESPACE CONFIGMAP SECRET" >&2
  exit 2
fi

namespace="$1"
configmap="$2"
secret="$3"

config_value() {
  kubectl -n "$namespace" get configmap "$configmap" \
    -o "jsonpath={.data.$1}"
}

secret_value() {
  kubectl -n "$namespace" get secret "$secret" \
    -o "jsonpath={.data.$1}"
}

fail() {
  echo "FAIL: transactional email preflight ($namespace): $1" >&2
  exit 1
}

[ "$(config_value SMTP_TEST_MODE)" = "false" ] || \
  fail "SMTP_TEST_MODE must be false"
[ -n "$(config_value SMTP_FROM)" ] || fail "sender is missing"
[ -n "$(config_value SMTP_TO)" ] || fail "clinic recipients are missing"

case "$(config_value EMAIL_TRANSPORT)" in
  brevo_api)
    encoded_key="$(secret_value BREVO_API_KEY)"
    [ -n "$encoded_key" ] || fail "BREVO_API_KEY is missing in secret/$secret"
    [ "$encoded_key" != 'Q0hBTkdFX01F' ] || \
      fail "BREVO_API_KEY is an example placeholder in secret/$secret"
    unset encoded_key
    ;;
  smtp)
    [ -n "$(config_value SMTP_HOST)" ] || fail "SMTP host is missing"
    for key in SMTP_USER SMTP_PASSWORD; do
      encoded_value="$(secret_value "$key")"
      [ -n "$encoded_value" ] || fail "$key is missing in secret/$secret"
      [ "$encoded_value" != 'Q0hBTkdFX01F' ] || \
        fail "$key is an example placeholder in secret/$secret"
      unset encoded_value
    done
    ;;
  *)
    fail "unsupported EMAIL_TRANSPORT"
    ;;
esac

echo "OK: transactional email configuration has the required fields ($namespace)."
