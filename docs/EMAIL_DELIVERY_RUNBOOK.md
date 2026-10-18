# Booking email incident checks

A `201` from `POST /api/v1/appointments` means the appointment was stored. It
does **not** prove that Brevo accepted the acknowledgement or that any mailbox
received it. Check the existing appointment in the authenticated admin portal
before trying another booking; a repeat request can create a duplicate.

## Configuration and logs

From an authorized Kubernetes management shell, in this repository:

```sh
sh scripts/check-email-config.sh drfarah drfarah-api-config drfarah-api-secret
sh scripts/check-email-config.sh drfarah-staging drfarah-staging-api-config drfarah-staging-api-secret
```

The command prints only whether the expected Secret fields exist. It cannot
validate a Brevo key, sender verification, acceptance, or final delivery.
Never print the Secret or paste a key into a build log or ticket.

Check errors near the reported booking time using a narrow log filter:

```sh
kubectl -n drfarah logs deployment/drfarah-api --since=24h |
  grep -E 'Brevo API|confirmation not accepted|notification not accepted|No clinic notification recipients|Unsupported email transport'
```

An absent `BREVO_API_KEY` is possible on older production installations: the
previous automatic bootstrap copied the SMTP rollback credentials but did not
populate the Brevo API key, while the active transport was `brevo_api`.
The CI preflight now blocks a new deployment with a missing key; the bootstrap
requires a separately supplied production key before creating fresh Secrets.

If the key is absent, an authorized operator should create a **production**
Brevo API key and add it to the existing `drfarah-api-secret` without replacing
the database or SMTP entries. Restart `deployment/drfarah-api` so its
environment reads the updated Secret. Do not use an SMTP key as an API key.
For a first deployment, pass the key as `DRFARAH_PROD_BREVO_API_KEY` through a
protected management environment when running
`scripts/bootstrap-production-secrets.sh`. Existing Secrets are never
overwritten by that script.

If the preflight passes but logs report a rejection, compare its HTTP status
and booking time with Brevo transactional logs. Confirm the sending address
`notifications@drfarahvipurgentcare.com` is verified, and check delivered,
bounced, blocked and deferred events for the three separate messages: patient
and two clinic recipients. A Brevo API `201`/message ID proves provider
acceptance, not inbox delivery. The staging CI smoke booking uses an
authenticated internal marker and deliberately skips sending email; it does
not establish live delivery.

Only after the secret and provider status are confirmed should an authorized
operator run one controlled real booking, inspect the patient and clinic
receipts, and verify the appointment in the secure admin portal. Keep patient
contact information out of issue comments and CI logs.
