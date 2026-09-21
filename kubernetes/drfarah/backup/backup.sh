#!/bin/sh

# Daily production PostgreSQL backup to the independent Hestia host.
# Secret values are consumed from Kubernetes environment variables and are
# never printed.

set -eu
umask 077

: "${POSTGRES_HOST:?POSTGRES_HOST is required}"
: "${POSTGRES_PORT:?POSTGRES_PORT is required}"
: "${POSTGRES_USER:?POSTGRES_USER is required}"
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD is required}"
: "${POSTGRES_DB:?POSTGRES_DB is required}"
: "${BACKUP_SSH_HOST:?BACKUP_SSH_HOST is required}"
: "${BACKUP_SSH_PORT:?BACKUP_SSH_PORT is required}"
: "${BACKUP_SSH_USER:?BACKUP_SSH_USER is required}"
: "${BACKUP_REMOTE_DIR:?BACKUP_REMOTE_DIR is required}"

key_file='/run/secrets/backup-ssh/id_ed25519'
known_hosts='/run/secrets/backup-ssh/known_hosts'

[ -s "$key_file" ] || {
  echo "FAIL: backup SSH private key is missing." >&2
  exit 1
}

[ -s "$known_hosts" ] || {
  echo "FAIL: backup SSH known_hosts file is missing." >&2
  exit 1
}

export PGPASSWORD="$POSTGRES_PASSWORD"

timestamp="$(date -u '+%Y%m%dT%H%M%SZ')"
backup_name="drfarah-${timestamp}-${HOSTNAME}.dump"
backup_file="/tmp/${backup_name}"

pg_dump \
  --format=custom \
  --no-owner \
  --no-privileges \
  --host="$POSTGRES_HOST" \
  --port="$POSTGRES_PORT" \
  --username="$POSTGRES_USER" \
  --dbname="$POSTGRES_DB" \
  --file="$backup_file"

pg_restore --list "$backup_file" >/dev/null

ssh_options="-i $key_file -p $BACKUP_SSH_PORT -o BatchMode=yes -o StrictHostKeyChecking=yes -o UserKnownHostsFile=$known_hosts"

ssh $ssh_options \
  "$BACKUP_SSH_USER@$BACKUP_SSH_HOST" \
  "mkdir -p '$BACKUP_REMOTE_DIR' && chmod 700 '$BACKUP_REMOTE_DIR'"

scp \
  -i "$key_file" \
  -P "$BACKUP_SSH_PORT" \
  -o BatchMode=yes \
  -o StrictHostKeyChecking=yes \
  -o UserKnownHostsFile="$known_hosts" \
  "$backup_file" \
  "$BACKUP_SSH_USER@$BACKUP_SSH_HOST:$BACKUP_REMOTE_DIR/$backup_name"

ssh $ssh_options \
  "$BACKUP_SSH_USER@$BACKUP_SSH_HOST" \
  "chmod 600 '$BACKUP_REMOTE_DIR/$backup_name' && find '$BACKUP_REMOTE_DIR' -type f -name 'drfarah-*.dump' -mtime +30 -delete"

echo "BACKUP_COMPLETE=$backup_name"
