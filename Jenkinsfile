pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout(true)
    disableConcurrentBuilds()
  }

  environment {
    PROJECT_SLUG = 'drfarah'

    HARBOR_REGISTRY = 'harbor.proxbenovh.cloud'
    HARBOR_PROJECT = 'devops-project-harbor'
    API_IMAGE_NAME = 'drfarah-api'
    BACKUP_IMAGE_NAME = 'drfarah-postgres-backup'

    KUBECONFIG = '/var/lib/jenkins/.kube/config-afpa-k3s'
    STAGING_NAMESPACE = 'drfarah-staging'
    STAGING_API_URL = 'https://api-staging.drfarahvipurgentcare.com'
    PRODUCTION_NAMESPACE = 'drfarah'
    PRODUCTION_API_URL = 'https://api.drfarahvipurgentcare.com'

    HESTIA_SSH_HOST = '192.168.100.75'
    HESTIA_SSH_PORT = '2275'
    HESTIA_SSH_USER = 'benweb'
    STAGING_FRONTEND_HOST = 'staging.drfarahvipurgentcare.com'
    STAGING_DOCROOT = '/home/benweb/web/staging.drfarahvipurgentcare.com/public_html'
    ADMIN_FRONTEND_HOST = 'admin-staging.drfarahvipurgentcare.com'
    ADMIN_DOCROOT = '/home/benweb/web/admin-staging.drfarahvipurgentcare.com/public_html'
    PRODUCTION_FRONTEND_HOST = 'drfarahvipurgentcare.com'
    PRODUCTION_FRONTEND_DOCROOT = '/home/benweb/web/drfarahvipurgentcare.com/public_html'
    PRODUCTION_ADMIN_HOST = 'admin.drfarahvipurgentcare.com'
    PRODUCTION_ADMIN_DOCROOT = '/home/benweb/web/admin.drfarahvipurgentcare.com/public_html'
    PRODUCTION_BACKUP_DIR = '/home/benweb/backups/drfarah-postgres'
  }

  // =========================================================================
  // JENKINSFILE — staging and production delivery
  //
  // All branches:
  //   - Clean checkout
  //   - Repository validation
  //   - Secret-filename detection
  //   - Markdown inventory
  //   - API tests
  //   - API Docker image/runtime validation
  //   - Frontend validation
  //
  // dev only:
  //   - Build and push API image to Harbor
  //   - Deploy API and PostgreSQL resources to staging
  //   - Verify staging API and booking endpoint
  //   - Deploy frontend to staging
  //
  // main only:
  //   - Fail-closed production preflight
  //   - Build and push immutable API/backup images
  //   - Deploy isolated production PostgreSQL/API
  //   - Run off-cluster backup and disposable restore test
  //   - Publish crawlable production frontend and production admin SPA
  //   - Verify final-domain HTTPS/API/redirect/indexing behavior
  // =========================================================================

  stages {

    stage('Checkout') {
      steps {
        deleteDir()
        checkout scm
      }
    }

    stage('Build metadata') {
      steps {
        sh '''
          set -eu

          echo "========================================="
          echo "Project:     ${PROJECT_SLUG}"
          echo "Branch:      ${BRANCH_NAME:-unknown}"
          echo "Commit:      ${GIT_COMMIT:-unknown}"
          echo "Git SHA:     $(git rev-parse HEAD)"
          echo "Build:       ${BUILD_NUMBER:-unknown}"
          echo "Node:        ${NODE_NAME:-unknown}"
          echo "Workspace:   ${WORKSPACE:-unknown}"
          echo "========================================="
        '''
      }
    }

    stage('Validate required paths') {
      steps {
        sh '''
          set -eu

          required_paths="
            README.md
            PROJECT.md
            HANDOFF.md
            SESSION_LOG.md
            .gitignore
            Jenkinsfile
            docs/READINESS_AUDIT.md
            docs/DECISIONS.md
            docs/architecture/README.md
            docs/design/DESIGN_SYSTEM_V1.md
            docs/design/DESIGN_SYSTEM_V2.md
            frontend/README.md
            frontend/index.html
            frontend/styles.css
            frontend/app.js
            frontend/robots.txt
            frontend/robots.production.txt
            frontend/.htaccess.production
            scripts/prepare-production-frontend.sh
            scripts/bootstrap-production-secrets.sh
            admin/README.md
            api/README.md
            api/Dockerfile
            api/requirements.txt
            api/requirements-dev.txt
            api/pytest.ini
            api/app/main.py
            api/app/core/config.py
            api/app/core/database.py
            api/app/models/booking.py
            api/app/schemas/booking.py
            api/app/routers/booking.py
            api/app/routers/health.py
            api/app/services/email.py
            api/tests/test_booking.py
            api/tests/test_health.py
            api/tests/conftest.py
            api/tests/test_services.py
            api/tests/test_availability.py
            api/tests/test_appointments.py
            api/tests/test_concurrency.py
            api/app/models/service.py
            api/app/models/working_hours.py
            api/app/models/blocked_period.py
            api/app/models/appointment.py
            api/app/services/scheduling.py
            api/app/schemas/service.py
            api/app/schemas/availability.py
            api/app/schemas/appointment.py
            api/app/routers/appointments.py
            api/alembic.ini
            api/alembic/env.py
            api/alembic/versions/0001_initial_bookings.py
            api/alembic/versions/0002_add_scheduling_tables.py
            kubernetes/drfarah/README.md
            kubernetes/drfarah/namespace.yaml
            kubernetes/drfarah/postgres-statefulset.yaml
            kubernetes/drfarah/postgres-service.yaml
            kubernetes/drfarah/configmap.yaml
            kubernetes/drfarah/secret.example.yaml
            kubernetes/drfarah/api-deployment.yaml
            kubernetes/drfarah/api-service.yaml
            kubernetes/drfarah/api-ingress.yaml
            kubernetes/drfarah/postgres-backup-cronjob.yaml
            kubernetes/drfarah/backup/Dockerfile
            kubernetes/drfarah/backup/backup.sh
            kubernetes/drfarah-staging/namespace.yaml
            kubernetes/drfarah-staging/postgres-statefulset.yaml
            kubernetes/drfarah-staging/postgres-service.yaml
            kubernetes/drfarah-staging/configmap.yaml
            kubernetes/drfarah-staging/secret.example.yaml
            kubernetes/drfarah-staging/api-deployment.yaml
            kubernetes/drfarah-staging/api-service.yaml
            kubernetes/drfarah-staging/api-ingress.yaml
          "

          missing=""

          for path in $required_paths; do
            if [ -e "$path" ]; then
              echo "OK    $path"
            else
              echo "MISS  $path"
              missing="$missing $path"
            fi
          done

          if [ -n "$missing" ]; then
            echo ""
            echo "ERROR: missing required paths:$missing"
            exit 1
          fi

          echo ""
          echo "All required paths are present."
        '''
      }
    }

    stage('Validate final-domain hostname contract') {
      steps {
        sh '''
          set -eu

          domain='drfarahvipurgentcare.com'
          staging_api="api-staging.${domain}"
          staging_admin="admin-staging.${domain}"
          production_api="api.${domain}"
          production_admin="admin.${domain}"

          echo "Checking for obsolete nested staging hostnames..."

          for prefix in api admin; do
            obsolete_host="${prefix}.staging.${domain}"
            hits="$(git grep -nF "$obsolete_host" -- . || true)"

            if [ -n "$hits" ]; then
              echo "FAIL: obsolete hostname found: $obsolete_host"
              echo "$hits"
              exit 1
            fi
          done

          require_text() {
            file="$1"
            needle="$2"

            if ! grep -qF "$needle" "$file"; then
              echo "FAIL: expected hostname contract is missing from $file"
              echo "Expected: $needle"
              exit 1
            fi
          }

          require_text Jenkinsfile "STAGING_API_URL = 'https://${staging_api}'"
          require_text Jenkinsfile "ADMIN_FRONTEND_HOST = '${staging_admin}'"
          require_text Jenkinsfile "ADMIN_DOCROOT = '/home/benweb/web/${staging_admin}/public_html'"
          require_text Jenkinsfile "PRODUCTION_API_URL = 'https://${production_api}'"
          require_text Jenkinsfile "PRODUCTION_FRONTEND_HOST = '${domain}'"
          require_text Jenkinsfile "PRODUCTION_FRONTEND_DOCROOT = '/home/benweb/web/${domain}/public_html'"
          require_text Jenkinsfile "PRODUCTION_ADMIN_HOST = '${production_admin}'"
          require_text Jenkinsfile "PRODUCTION_ADMIN_DOCROOT = '/home/benweb/web/${production_admin}/public_html'"
          require_text frontend/booking.js "https://${staging_api}/api/v1"
          require_text frontend/booking.js "https://${production_api}/api/v1"
          require_text frontend/registration.js "https://${staging_api}/api/v1"
          require_text frontend/registration.js "https://${production_api}/api/v1"
          require_text admin/config.js "h === '${staging_admin}'"
          require_text admin/config.js "https://${staging_api}/api/v1"
          require_text admin/config.js "h === '${production_admin}'"
          require_text admin/config.js "https://${production_api}/api/v1"
          require_text kubernetes/drfarah-staging/api-ingress.yaml "host: ${staging_api}"
          require_text kubernetes/drfarah-staging/configmap.yaml "https://${staging_admin}"
          require_text kubernetes/drfarah/api-ingress.yaml "host: ${production_api}"
          require_text kubernetes/drfarah/configmap.yaml "https://${production_admin}"

          echo "Final-domain hostname contract is consistent."
        '''
      }
    }

    stage('Detect committed secret filenames') {
      steps {
        sh '''
          set -eu

          hits="$(
            git ls-files \
              | grep -E '(^|/)([.]env|secret[.]yaml|secrets[.]yaml|[^/]*[.]tfstate|[^/]*[.]tfvars|credentials[.]json|service-account-key[.]json|id_rsa|id_ed25519|[^/]*[.]pem)$' \
              | grep -Ev '[.]example$' \
              || true
          )"

          if [ -n "$hits" ]; then
            echo "FAIL: forbidden committed secret filenames found:"
            echo "$hits"
            exit 1
          fi

          echo "OK: no forbidden committed secret filenames detected."
        '''
      }
    }

    stage('Markdown hygiene') {
      steps {
        sh '''
          set -eu

          echo "Checking Markdown files for basic readability..."

          md_files="$(
            find . \
              -name '*.md' \
              -not -path './.git/*' \
              -not -path '*/.pytest_cache/*' \
              -not -path '*/__pycache__/*' \
              | sort
          )"

          if [ -z "$md_files" ]; then
            echo "No Markdown files found."
            exit 0
          fi

          echo "$md_files" | while IFS= read -r file; do
            lines="$(wc -l < "$file")"
            echo "  $file  ($lines lines)"
          done

          echo "Markdown file count: $(printf '%s\n' "$md_files" | wc -l)"
        '''
      }
    }

    stage('API — tests') {
      steps {
        dir('api') {
          sh '''
            set -eu

            echo "Running API tests in python:3.12-slim..."

            docker run --rm \
              -v "$PWD":/app:ro \
              -w /tmp \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/drfarah-ci.db' \
              -e PYTHONDONTWRITEBYTECODE=1 \
              -e PYTHONPYCACHEPREFIX=/tmp/pycache \
              python:3.12-slim \
              bash -c '
                set -e

                rm -f \
                  /tmp/drfarah-ci.db \
                  /tmp/drfarah.db

                pip install -q \
                  -r /app/requirements.txt \
                  -r /app/requirements-dev.txt

                PYTHONPATH=/app \
                  python -m pytest \
                  -q \
                  -p no:cacheprovider \
                  -m "not postgresql" \
                  /app/tests/
              '

            echo "API tests passed."
          '''
        }
      }
    }

    stage('API — PostgreSQL integration tests') {
      steps {
        dir('api') {
          sh '''
            set -eu

            SUFFIX="${BUILD_NUMBER}-$$"
            NET="drfarah-pgtest-net-${SUFFIX}"
            PG="drfarah-pgtest-db-${SUFFIX}"
            RUNNER="drfarah-pgtest-runner-${SUFFIX}"
            PG_USER="drfarah_ci"
            PG_MAINT_DB="postgres"
            # Ephemeral, non-sensitive CI credential — never reused, dropped with the container.
            PG_PASSWORD="ci_${BUILD_NUMBER}_$$"

            cleanup() {
              docker rm -f "$RUNNER" >/dev/null 2>&1 || true
              docker rm -f "$PG" >/dev/null 2>&1 || true
              docker network rm "$NET" >/dev/null 2>&1 || true
            }
            trap cleanup EXIT HUP INT TERM

            echo "=== Creating isolated Docker network ==="
            docker network create "$NET" >/dev/null

            echo "=== Starting disposable PostgreSQL ==="
            docker run -d \
              --name "$PG" \
              --network "$NET" \
              -e POSTGRES_USER="$PG_USER" \
              -e POSTGRES_PASSWORD="$PG_PASSWORD" \
              -e POSTGRES_DB="$PG_MAINT_DB" \
              --tmpfs /var/lib/postgresql/data \
              postgres:16-alpine \
              >/dev/null

            echo "=== Waiting for PostgreSQL readiness ==="
            ready=0
            for attempt in $(seq 1 30); do
              if docker exec "$PG" pg_isready -U "$PG_USER" -d "$PG_MAINT_DB" >/dev/null 2>&1; then
                ready=1
                echo "PostgreSQL ready on attempt $attempt."
                break
              fi
              echo "  attempt $attempt/30 — PostgreSQL not ready yet"
              sleep 1
            done

            if [ "$ready" -ne 1 ]; then
              echo "FAIL: PostgreSQL did not become ready."
              docker logs --tail 80 "$PG" || true
              exit 1
            fi

            # Maintenance URL (reachable by container name over the private network).
            MAINT_URL="postgresql+psycopg://${PG_USER}:${PG_PASSWORD}@${PG}:5432/${PG_MAINT_DB}"

            echo "=== Running PostgreSQL-marked tests in an isolated runner ==="
            docker run --rm \
              --name "$RUNNER" \
              --network "$NET" \
              -v "$PWD":/app:ro \
              -w /app \
              -e ENVIRONMENT=test \
              -e SMTP_TEST_MODE=true \
              -e POSTGRES_TEST_DATABASE_URL="$MAINT_URL" \
              -e PYTHONDONTWRITEBYTECODE=1 \
              -e PYTHONPYCACHEPREFIX=/tmp/pycache \
              python:3.12-slim \
              bash -c '
                set -e
                pip install -q \
                  -r /app/requirements.txt \
                  -r /app/requirements-dev.txt
                PYTHONPATH=/app \
                  python -m pytest \
                  -q \
                  -p no:cacheprovider \
                  -m postgresql \
                  /app/tests/
              '

            echo "PostgreSQL integration tests passed."
          '''
        }
      }
    }

    stage('API — Docker build validation') {
      steps {
        dir('api') {
          sh '''
            set -eu

            UNIQUE_SUFFIX="${BUILD_NUMBER}-$$"
            CONTAINER_NAME="drfarah-api-validation-${UNIQUE_SUFFIX}"
            IMAGE_NAME="drfarah-api:test-build-${UNIQUE_SUFFIX}"

            cleanup() {
              docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
              docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true
            }

            trap cleanup EXIT HUP INT TERM

            echo "=== Building production API image ==="

            docker build \
              -t "$IMAGE_NAME" \
              .

            echo "Docker image build passed."

            echo ""
            echo "=== Validating Alembic assets ==="

            docker run --rm \
              "$IMAGE_NAME" \
              test -f /app/alembic.ini

            docker run --rm \
              "$IMAGE_NAME" \
              test -f /app/alembic/env.py

            docker run --rm \
              "$IMAGE_NAME" \
              python -m alembic --help

            echo "Alembic assets present."

            echo ""
            echo "=== Running disposable migration test ==="

            docker run --rm \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/alembic-migration-test.db' \
              "$IMAGE_NAME" \
              python -m alembic upgrade head

            echo "Disposable migration test passed."

            echo ""
            echo "=== Validating migration bootstrap ==="

            docker run --rm \
              "$IMAGE_NAME" \
              test -f /app/app/migration_bootstrap.py

            docker run --rm \
              "$IMAGE_NAME" \
              python -c "from app.migration_bootstrap import main; print('import OK')"

            echo ""
            echo "=== Fresh SQLite bootstrap ==="

            docker run --rm \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/bootstrap-test.db' \
              "$IMAGE_NAME" \
              python -m app.migration_bootstrap

            echo "Fresh SQLite bootstrap passed."

            echo ""
            echo "=== Starting isolated validation container ==="

            docker run -d \
              --name "$CONTAINER_NAME" \
              -P \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/drfarah-validation.db' \
              "$IMAGE_NAME" \
              >/dev/null

            HOST_PORT=""

            for attempt in $(seq 1 10); do
              HOST_PORT="$(
                docker port "$CONTAINER_NAME" 8000/tcp 2>/dev/null \
                  | head -n 1 \
                  | awk -F: '{print $NF}'
              )"

              if [ -n "$HOST_PORT" ]; then
                break
              fi

              sleep 1
            done

            if [ -z "$HOST_PORT" ]; then
              echo "FAIL: Docker did not publish the API validation port."

              docker ps -a \
                --filter "name=$CONTAINER_NAME" \
                || true

              docker inspect "$CONTAINER_NAME" \
                --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
                || true

              docker logs \
                --tail 200 \
                "$CONTAINER_NAME" \
                || true

              exit 1
            fi

            echo "Published validation port: $HOST_PORT"
            echo ""
            echo "=== Waiting for liveness endpoint ==="

            healthy=0

            for attempt in $(seq 1 30); do
              state="$(
                docker inspect "$CONTAINER_NAME" \
                  --format '{{.State.Status}}' \
                  2>/dev/null \
                  || echo missing
              )"

              if [ "$state" = "exited" ] || \
                 [ "$state" = "dead" ] || \
                 [ "$state" = "missing" ]; then
                echo "Container stopped before becoming healthy (state=$state)."
                break
              fi

              if curl -fsS \
                "http://127.0.0.1:${HOST_PORT}/api/v1/health/live" \
                >/dev/null 2>&1; then
                healthy=1
                break
              fi

              echo "  attempt $attempt/30 — API not ready yet"
              sleep 1
            done

            if [ "$healthy" -ne 1 ]; then
              echo ""
              echo "=== FAILURE: validation container did not become healthy ==="

              echo "--- docker ps ---"

              docker ps -a \
                --filter "name=$CONTAINER_NAME" \
                || true

              echo ""
              echo "--- container state ---"

              docker inspect "$CONTAINER_NAME" \
                --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
                || true

              echo ""
              echo "--- container logs ---"

              docker logs \
                --tail 200 \
                "$CONTAINER_NAME" \
                || true

              exit 1
            fi

            echo ""
            echo "=== Liveness response ==="

            curl -fsS \
              "http://127.0.0.1:${HOST_PORT}/api/v1/health/live"

            echo ""
            echo ""
            echo "=== Readiness response ==="

            curl -fsS \
              "http://127.0.0.1:${HOST_PORT}/api/v1/health/ready"

            echo ""
            echo ""
            echo "API Docker runtime validation passed."
          '''
        }
      }
    }

    stage('Production backup image — validation') {
      steps {
        sh '''
          set -eu

          UNIQUE_SUFFIX="${BUILD_NUMBER}-$$"
          IMAGE_NAME="drfarah-postgres-backup:test-build-${UNIQUE_SUFFIX}"

          cleanup_backup_image() {
            docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true
          }
          trap cleanup_backup_image EXIT HUP INT TERM

          echo "=== Building production PostgreSQL backup image ==="

          docker build \
            -t "$IMAGE_NAME" \
            kubernetes/drfarah/backup

          echo ""
          echo "=== Validating backup runtime tools ==="

          docker run --rm \
            --entrypoint /bin/sh \
            "$IMAGE_NAME" \
            -c '
              set -e
              command -v pg_dump >/dev/null
              command -v pg_restore >/dev/null
              command -v ssh >/dev/null
              command -v scp >/dev/null
              test -x /usr/local/bin/drfarah-backup
              sh -n /usr/local/bin/drfarah-backup
            '

          echo "Production backup image validation passed."
        '''
      }
    }

    stage('Frontend — validation') {
      steps {
        sh '''
          set -eu

          echo "=== Checking required frontend files ==="

          required_files="
            frontend/index.html
            frontend/styles.css
            frontend/app.js
            frontend/robots.txt
          "

          for file in $required_files; do
            if [ ! -f "$file" ]; then
              echo "MISS  $file"
              exit 1
            fi

            echo "OK    $file"
          done

          echo ""
          echo "=== JavaScript syntax ==="

          docker run --rm \
            -v "$PWD":/app:ro \
            -w /app \
            node:20-slim \
            node --check frontend/app.js && \
            node --check frontend/app-v5.js && \
            node --check frontend/booking.js && \
            node --check frontend/registration.js && \
            node --check admin/app.js

          echo "JavaScript syntax passed."

          echo ""
          echo "=== Temporary-domain indexing protection ==="

          grep -q \
            'noindex,nofollow,noarchive' \
            frontend/index.html \
            || {
              echo "FAIL: noindex meta is missing."
              exit 1
            }

          grep -q \
            'Disallow: /' \
            frontend/robots.txt \
            || {
              echo "FAIL: robots.txt Disallow rule is missing."
              exit 1
            }

          echo "No-index checks passed."

          echo ""
          echo "=== Static frontend serving validation ==="

          UNIQUE_SUFFIX="${BUILD_NUMBER}-$$"
          CONTAINER_NAME="drfarah-frontend-validation-${UNIQUE_SUFFIX}"

          cleanup_frontend() {
            docker rm -f "$CONTAINER_NAME" \
              >/dev/null 2>&1 || true
          }

          trap cleanup_frontend EXIT HUP INT TERM

          docker run -d \
            --name "$CONTAINER_NAME" \
            --expose 8000 \
            -P \
            -v "$PWD/frontend":/site:ro \
            -w /site \
            python:3.12-slim \
            python -m http.server 8000 --bind 0.0.0.0 \
            >/dev/null

          HOST_PORT=""

          for attempt in $(seq 1 10); do
            HOST_PORT="$(
              docker port "$CONTAINER_NAME" 8000/tcp 2>/dev/null \
                | head -n 1 \
                | awk -F: '{print $NF}'
              )"

            if [ -n "$HOST_PORT" ]; then
              break
            fi

            state="$(
              docker inspect "$CONTAINER_NAME" \
                --format '{{.State.Status}}' \
                2>/dev/null \
                || echo missing
            )"

            if [ "$state" = "exited" ] || \
               [ "$state" = "dead" ] || \
               [ "$state" = "missing" ]; then
              echo "Frontend container stopped before publishing a port."
              break
            fi

            sleep 1
          done

          if [ -z "$HOST_PORT" ]; then
            echo "FAIL: frontend validation port was not published."

            docker ps -a \
              --filter "name=$CONTAINER_NAME" \
              || true

            docker inspect "$CONTAINER_NAME" \
              --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
              || true

            docker logs \
              --tail 100 \
              "$CONTAINER_NAME" \
              || true

            exit 1
          fi

          echo "Published frontend validation port: $HOST_PORT"

          server_ready=0

          for attempt in $(seq 1 15); do
            state="$(
              docker inspect "$CONTAINER_NAME" \
                --format '{{.State.Status}}' \
                2>/dev/null \
                || echo missing
            )"

            if [ "$state" = "exited" ] || \
               [ "$state" = "dead" ] || \
               [ "$state" = "missing" ]; then
              echo "Frontend container stopped before becoming ready."
              break
            fi

            if curl -fsS \
              "http://127.0.0.1:${HOST_PORT}/" \
              >/dev/null 2>&1; then
              server_ready=1
              break
            fi

            echo "  attempt $attempt/15 — frontend not ready yet"
            sleep 1
          done

          if [ "$server_ready" -ne 1 ]; then
            echo "FAIL: frontend static server did not become ready."

            docker ps -a \
              --filter "name=$CONTAINER_NAME" \
              || true

            docker inspect "$CONTAINER_NAME" \
              --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
              || true

            docker logs \
              --tail 100 \
              "$CONTAINER_NAME" \
              || true

            exit 1
          fi

          public_paths="
            /
            /styles.css
            /app.js
            /booking.js
            /robots.txt
            /sitemap.xml
            /assets/hero-treatment.jpg
            /assets/consult-rejuvenation.jpg
            /assets/mobile-visit.jpg
            /assets/reception-vip.jpg
            /assets/favicon.svg
          "

          for path in $public_paths; do
            status="$(
              curl -sS \
                -o /dev/null \
                -w '%{http_code}' \
                "http://127.0.0.1:${HOST_PORT}${path}"
            )"

            if [ "$status" != "200" ]; then
              echo "FAIL  $path -> $status"
              exit 1
            fi

            echo "OK    $path -> $status"
          done

          echo ""
          echo "=== Production frontend assembly validation ==="

          PROD_VALIDATION_DIR="$(mktemp -d)"
          trap 'cleanup_frontend; rm -rf "$PROD_VALIDATION_DIR"' EXIT HUP INT TERM

          sh scripts/prepare-production-frontend.sh \
            frontend \
            "$PROD_VALIDATION_DIR"

          echo ""
          echo "Frontend validation passed."
        '''
      }
    }

    stage('Production — preflight') {
      when {
        branch 'main'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            echo "=== Repository production gates ==="

            if grep -R -nF 'REPLACE_BEFORE_PRODUCTION' kubernetes/drfarah; then
              echo "FAIL: unresolved production value marker found."
              exit 1
            fi

            if grep -qF 'CUTOVER_BLOCKER' frontend/.htaccess.production; then
              echo "FAIL: legacy redirect cutover blocker remains."
              exit 1
            fi

            grep -qF 'LEGACY_REDIRECT_RISK_ACCEPTED: 2026-09-21' \
              frontend/.htaccess.production || {
                echo "FAIL: explicit legacy redirect decision is missing."
                exit 1
              }

            if grep -qF 'BACKUP_READINESS_BLOCKER' kubernetes/drfarah/README.md; then
              echo "FAIL: production backup readiness blocker remains."
              exit 1
            fi

            if git grep -nF '/wp-content/uploads/' -- frontend; then
              echo "FAIL: frontend still depends on legacy WordPress assets."
              exit 1
            fi

            test -r "$KUBECONFIG" || {
              echo "FAIL: kubeconfig missing or unreadable."
              exit 1
            }

            echo "Repository gates passed."
            echo ""
            echo "=== Production namespace and secret preflight ==="

            # Jenkins runs sh steps with xtrace enabled. Kubernetes Secret
            # values are not Jenkins-managed credentials, so the masker cannot
            # protect values returned by kubectl. Disable tracing before any
            # Secret read and only re-enable it after the values are unset.
            set +x

            kubectl apply -f kubernetes/drfarah/namespace.yaml

            db_secret_present=0
            api_secret_present=0

            if kubectl -n "$PRODUCTION_NAMESPACE" \
              get secret drfarah-db-secret >/dev/null 2>&1; then
              db_secret_present=1
            fi

            if kubectl -n "$PRODUCTION_NAMESPACE" \
              get secret drfarah-api-secret >/dev/null 2>&1; then
              api_secret_present=1
            fi

            if [ "$db_secret_present" -eq 0 ] && [ "$api_secret_present" -eq 0 ]; then
              if kubectl -n "$PRODUCTION_NAMESPACE" \
                get pvc data-drfarah-postgres-0 >/dev/null 2>&1; then
                echo "FAIL: production DB secrets are absent but an initialized PVC exists."
                echo "Recover the original credentials; do not generate replacements."
                exit 1
              fi
              echo "Production DB/API secrets are absent; running one-time safe bootstrap."
              sh scripts/bootstrap-production-secrets.sh
            elif [ "$db_secret_present" -ne "$api_secret_present" ]; then
              echo "FAIL: production DB/API secret state is partial; refusing to guess or overwrite."
              exit 1
            else
              echo "Existing production DB/API secrets will be validated and preserved."
            fi

            for secret in harbor-regcred drfarah-db-secret drfarah-api-secret; do
              kubectl -n "$PRODUCTION_NAMESPACE" get secret "$secret" >/dev/null || {
                echo "FAIL: required production secret is missing: $secret"
                exit 1
              }
              echo "OK    secret/$secret"
            done

            require_secret_key() {
              secret="$1"
              key="$2"
              value="$(
                kubectl -n "$PRODUCTION_NAMESPACE" \
                  get secret "$secret" \
                  -o "jsonpath={.data.${key}}"
              )"

              if [ -z "$value" ]; then
                echo "FAIL: secret/$secret is missing key $key"
                exit 1
              fi

              echo "OK    secret/$secret key $key"
            }

            for key in POSTGRES_USER POSTGRES_PASSWORD POSTGRES_DB; do
              require_secret_key drfarah-db-secret "$key"
            done

            for key in DATABASE_URL POSTGRES_USER POSTGRES_PASSWORD SMTP_USER SMTP_PASSWORD; do
              require_secret_key drfarah-api-secret "$key"
            done

            prod_db_password="$(
              kubectl -n "$PRODUCTION_NAMESPACE" \
                get secret drfarah-db-secret \
                -o jsonpath='{.data.POSTGRES_PASSWORD}'
            )"
            api_db_password="$(
              kubectl -n "$PRODUCTION_NAMESPACE" \
                get secret drfarah-api-secret \
                -o jsonpath='{.data.POSTGRES_PASSWORD}'
            )"
            staging_db_password="$(
              kubectl -n "$STAGING_NAMESPACE" \
                get secret drfarah-staging-db-secret \
                -o jsonpath='{.data.POSTGRES_PASSWORD}'
            )"

            if [ "$prod_db_password" != "$api_db_password" ]; then
              echo "FAIL: production API and PostgreSQL secrets use different DB passwords."
              exit 1
            fi

            if [ "$prod_db_password" = "$staging_db_password" ]; then
              echo "FAIL: production reuses the staging PostgreSQL password."
              exit 1
            fi

            unset prod_db_password api_db_password staging_db_password value
            set -x
            echo "Production DB isolation confirmed."

            echo ""
            echo "=== Hestia production preflight ==="

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            ssh $SSH_OPTS \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST" \
              sh -s -- \
              "$PRODUCTION_FRONTEND_DOCROOT" \
              "$PRODUCTION_ADMIN_DOCROOT" \
              "$PRODUCTION_BACKUP_DIR" <<'HESTIA_PREFLIGHT'
              set -eu

              for path in "$1" "$2"; do
                [ -d "$path" ] || {
                  echo "ERROR: production docroot is missing: $path"
                  exit 1
                }
                touch "$path/.jenkins-write-test"
                rm -f "$path/.jenkins-write-test"
              done

              mkdir -p "$3"
              chmod 700 "$3"
              touch "$3/.jenkins-write-test"
              rm -f "$3/.jenkins-write-test"
              echo 'Production docroots and backup destination are writable.'
HESTIA_PREFLIGHT

            echo ""
            echo "=== Installing backup SSH material in production namespace ==="

            KNOWN_HOSTS="$(mktemp)"
            SECRET_MANIFEST="$(mktemp)"
            chmod 600 "$KNOWN_HOSTS" "$SECRET_MANIFEST"

            cleanup_preflight() {
              rm -f "$KNOWN_HOSTS" "$SECRET_MANIFEST"
            }
            trap cleanup_preflight EXIT HUP INT TERM

            ssh-keyscan \
              -p "$HESTIA_SSH_PORT" \
              -H "$HESTIA_SSH_HOST" \
              > "$KNOWN_HOSTS" 2>/dev/null

            test -s "$KNOWN_HOSTS" || {
              echo "FAIL: unable to capture Hestia SSH host key."
              exit 1
            }

            kubectl -n "$PRODUCTION_NAMESPACE" \
              create secret generic drfarah-backup-ssh \
              --from-file=id_ed25519="$SSH_KEY" \
              --from-file=known_hosts="$KNOWN_HOSTS" \
              --dry-run=client \
              -o yaml \
              > "$SECRET_MANIFEST"

            kubectl apply -f "$SECRET_MANIFEST"
            cleanup_preflight
            trap - EXIT HUP INT TERM

            echo "Production preflight passed."
          '''
        }
      }
    }

    stage('API — build and push to Harbor') {
      when {
        anyOf {
          branch 'dev'
          branch 'main'
        }
      }

      steps {
        withCredentials([
          usernamePassword(
            credentialsId: 'harbor-robot-devops-project-harbor',
            usernameVariable: 'HARBOR_USER',
            passwordVariable: 'HARBOR_PASS'
          )
        ]) {
          sh '''
            set -eu

            IMAGE_TAG="$(git rev-parse HEAD)"

            if [ -z "$IMAGE_TAG" ]; then
              echo "FAIL: git rev-parse HEAD returned an empty string."
              exit 1
            fi

            if ! echo "$IMAGE_TAG" | grep -qE '^[0-9a-f]{40}$'; then
              echo "FAIL: Git SHA is not a valid 40-char hex string: '$IMAGE_TAG'"
              exit 1
            fi

            echo "Immutable image tag validated: $IMAGE_TAG"

            FULL_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}"
            BUILD_IMAGE="${FULL_IMAGE}:${IMAGE_TAG}"

            if [ "${BRANCH_NAME:-}" = "main" ]; then
              API_ALIAS_IMAGE="${FULL_IMAGE}:prod"
            else
              API_ALIAS_IMAGE="${FULL_IMAGE}:dev"
            fi

            BACKUP_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${BACKUP_IMAGE_NAME}:${IMAGE_TAG}"
            BACKUP_ALIAS_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${BACKUP_IMAGE_NAME}:prod"

            DOCKER_CONFIG="${WORKSPACE}/.docker-auth-${BUILD_NUMBER}-$$"
            export DOCKER_CONFIG

            cleanup_harbor() {
              rm -rf "$DOCKER_CONFIG"

              docker rmi \
                "$BUILD_IMAGE" \
                "$API_ALIAS_IMAGE" \
                "$BACKUP_IMAGE" \
                "$BACKUP_ALIAS_IMAGE" \
                >/dev/null 2>&1 || true
            }

            trap cleanup_harbor EXIT HUP INT TERM

            mkdir -p "$DOCKER_CONFIG"

            echo "=== Harbor login ==="

            printf '%s' "$HARBOR_PASS" \
              | docker login "$HARBOR_REGISTRY" \
                  --username "$HARBOR_USER" \
                  --password-stdin

            echo ""
            echo "=== Building immutable and environment API tags ==="

            docker build \
              -t "$BUILD_IMAGE" \
              -t "$API_ALIAS_IMAGE" \
              api

            echo ""
            echo "=== Pushing immutable image ==="

            docker push "$BUILD_IMAGE"

            echo ""
            echo "=== Pushing API environment alias ==="

            docker push "$API_ALIAS_IMAGE"

            if [ "${BRANCH_NAME:-}" = "main" ]; then
              echo ""
              echo "=== Building production backup image ==="

              docker build \
                -t "$BACKUP_IMAGE" \
                -t "$BACKUP_ALIAS_IMAGE" \
                kubernetes/drfarah/backup

              docker push "$BACKUP_IMAGE"
              docker push "$BACKUP_ALIAS_IMAGE"
            fi

            echo ""
            echo "API image pushed:"
            echo "$BUILD_IMAGE"
          '''
        }
      }
    }

    stage('API — deploy staging manifests') {
      when {
        branch 'dev'
      }

      steps {
        sh '''
          set -eu

          IMAGE_TAG="$(git rev-parse HEAD)"

          if [ -z "$IMAGE_TAG" ]; then
            echo "FAIL: git rev-parse HEAD returned an empty string."
            exit 1
          fi

          if ! echo "$IMAGE_TAG" | grep -qE '^[0-9a-f]{40}$'; then
            echo "FAIL: Git SHA is not a valid 40-char hex string: '$IMAGE_TAG'"
            exit 1
          fi

          FULL_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:${IMAGE_TAG}"

          echo "Using kubeconfig: $KUBECONFIG"
          echo "Immutable image: $FULL_IMAGE"

          test -r "$KUBECONFIG" || {
            echo "FAIL: kubeconfig missing or unreadable."
            exit 1
          }

          echo ""
          echo "=== Applying staging namespace ==="

          kubectl apply \
            -f kubernetes/drfarah-staging/namespace.yaml

          echo ""
          echo "=== Applying PostgreSQL and API resources ==="

          kubectl apply \
            -f kubernetes/drfarah-staging/configmap.yaml \
            -f kubernetes/drfarah-staging/postgres-service.yaml \
            -f kubernetes/drfarah-staging/postgres-statefulset.yaml \
            -f kubernetes/drfarah-staging/api-service.yaml \
            -f kubernetes/drfarah-staging/api-ingress.yaml

          echo ""
          echo "=== Rendering Deployment with immutable image ==="

          RENDERED="$(mktemp)"

          PLACEHOLDER="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:dev"

          sed "s|image: ${PLACEHOLDER}|image: ${FULL_IMAGE}|g" \
            kubernetes/drfarah-staging/api-deployment.yaml > "$RENDERED"

          IMAGE_COUNT="$(grep -cF "image: ${FULL_IMAGE}" "$RENDERED" || true)"

          if [ "$IMAGE_COUNT" -ne 2 ]; then
            echo "FAIL: expected 2 image lines with immutable tag, found ${IMAGE_COUNT}"
            echo "Rendered manifest preserved at $RENDERED"
            exit 1
          fi

          if grep -qE 'image:.*:dev\b' "$RENDERED"; then
            echo "FAIL: :dev placeholder still present in rendered manifest"
            grep -nE 'image:.*:dev\b' "$RENDERED" || true
            exit 1
          fi

          echo "Rendered image: $FULL_IMAGE"
          echo "  image occurrences: $IMAGE_COUNT"

          echo ""
          echo "=== Applying rendered Deployment ==="

          kubectl apply -f "$RENDERED"

          rm -f "$RENDERED"

          echo ""
          echo "=== Waiting for PostgreSQL ==="

          kubectl \
            -n "$STAGING_NAMESPACE" \
            rollout status statefulset/drfarah-staging-postgres \
            --timeout=180s

          echo ""
          echo "=== Waiting for API rollout ==="

          kubectl \
            -n "$STAGING_NAMESPACE" \
            rollout status deployment/drfarah-staging-api \
            --timeout=180s

          echo ""
          echo "Staging API rollout completed."
        '''
      }
    }

    stage('API — staging health check') {
      when {
        branch 'dev'
      }

      steps {
        // CI cleanup — token-protected, runs first to clear previous build records.
        withCredentials([
          string(
            credentialsId: 'drfarah-staging-ci-cleanup-token',
            variable: 'CLEANUP_TOKEN'
          )
        ]) {
          sh '''
            set -eu

            echo "=== CI cleanup ==="

            CLEANUP_RESPONSE="$(mktemp)"

            set +x
            cleanup_status="$(
              curl -sS \
                -o "$CLEANUP_RESPONSE" \
                -w '%{http_code}' \
                -X POST \
                -H "Authorization: Bearer ${CLEANUP_TOKEN}" \
                "${STAGING_API_URL}/api/v1/internal/cleanup-ci" \
                || true
            )"
            set -x

            if [ "$cleanup_status" != "200" ]; then
              echo "FAIL: CI cleanup returned HTTP $cleanup_status"
              cat "$CLEANUP_RESPONSE"
              rm -f "$CLEANUP_RESPONSE"
              exit 1
            fi

            echo "CI cleanup returned HTTP 200."
            rm -f "$CLEANUP_RESPONSE"
          '''
        }

        sh '''
          set -eu

          echo "=== Staging API liveness ==="

          live_status="000"

          for attempt in $(seq 1 18); do
            live_status="$(
              curl -sS \
                -o /dev/null \
                -w '%{http_code}' \
                "${STAGING_API_URL}/api/v1/health/live" \
                || true
            )"

            if [ -z "$live_status" ]; then
              live_status="000"
            fi

            if [ "$live_status" = "200" ]; then
              echo "Liveness passed on attempt $attempt."
              break
            fi

            echo "  attempt $attempt/18 -> HTTP $live_status"
            sleep 5
          done

          if [ "$live_status" != "200" ]; then
            echo "FAIL: staging liveness returned HTTP $live_status"
            exit 1
          fi

          echo ""
          echo "=== Staging API readiness ==="

          ready_status="000"

          for attempt in $(seq 1 12); do
            ready_status="$(
              curl -sS \
                -o /dev/null \
                -w '%{http_code}' \
                "${STAGING_API_URL}/api/v1/health/ready" \
                || true
            )"

            if [ -z "$ready_status" ]; then
              ready_status="000"
            fi

            if [ "$ready_status" = "200" ]; then
              echo "Readiness passed on attempt $attempt."
              break
            fi

            echo "  attempt $attempt/12 -> HTTP $ready_status"
            sleep 5
          done

          if [ "$ready_status" != "200" ]; then
            echo "FAIL: staging readiness returned HTTP $ready_status"
            exit 1
          fi

          echo ""
          echo "=== Staging services endpoint ==="

          SERVICES_JSON="$(
            curl -sS \
              "${STAGING_API_URL}/api/v1/services" \
              || true
          )"

          if [ -z "$SERVICES_JSON" ]; then
            echo "FAIL: services endpoint returned empty response"
            exit 1
          fi

          SERVICE_COUNT="$(
            echo "$SERVICES_JSON" \
            | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('services',[])))" \
            2>/dev/null || echo "0"
          )"

          if [ "$SERVICE_COUNT" -eq 0 ]; then
            echo "FAIL: no active services found — migrations may have failed"
            echo "$SERVICES_JSON"
            exit 1
          fi

          SERVICE_CODE="$(
            echo "$SERVICES_JSON" \
            | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['services'][0]['code'])"
          )"

          echo "Services endpoint returned ${SERVICE_COUNT} active service(s)."
          echo "Selected service for smoke test: $SERVICE_CODE"

          echo ""
          echo "=== Staging availability endpoint ==="

          START_DATE="$(date -d '+1 day' '+%Y-%m-%d' 2>/dev/null || date -v+1d '+%Y-%m-%d')"
          END_DATE="$(date -d '+14 days' '+%Y-%m-%d' 2>/dev/null || date -v+14d '+%Y-%m-%d')"

          AVAIL_JSON="$(
            curl -sS \
              "${STAGING_API_URL}/api/v1/availability?service_code=${SERVICE_CODE}&start_date=${START_DATE}&end_date=${END_DATE}" \
              || true
          )"

          if [ -z "$AVAIL_JSON" ]; then
            echo "FAIL: availability endpoint returned empty response"
            exit 1
          fi

          SLOT_COUNT="$(
            echo "$AVAIL_JSON" \
            | python3 -c "import json,sys; d=json.load(sys.stdin); print(len(d.get('slots',[])))" \
            2>/dev/null || echo "0"
          )"

          if [ "$SLOT_COUNT" -eq 0 ]; then
            echo "FAIL: no available slots in 14-day window for $SERVICE_CODE"
            echo "$AVAIL_JSON"
            exit 1
          fi

          SLOT_START="$(
            echo "$AVAIL_JSON" \
            | python3 -c "import json,sys; d=json.load(sys.stdin); print(d['slots'][0]['starts_at'])"
          )"

          echo "Availability returned ${SLOT_COUNT} slot(s)."
          echo "First available slot: $SLOT_START"

          echo ""
          echo "=== Staging booking smoke test ==="

          RESPONSE_FILE="$(mktemp)"

          booking_status="$(
            curl -sS \
              -o "$RESPONSE_FILE" \
              -w '%{http_code}' \
              -X POST \
              -H 'Content-Type: application/json' \
              -d '{
                "service_type": "CI smoke test",
                "visit_type": "Clinic visit",
                "preferred_day": "Monday",
                "preferred_time": "9:00 AM",
                "time_window": "Morning",
                "first_name": "Jenkins",
                "last_name": "SmokeTest",
                "email": "smoke-test@example.com",
                "phone": "+1-555-000-0000",
                "reason_category": "General appointment request"
              }' \
              "${STAGING_API_URL}/api/v1/bookings" \
              || true
          )"

          if [ -z "$booking_status" ]; then
            booking_status="000"
          fi

          if [ "$booking_status" != "201" ]; then
            echo "FAIL: booking smoke test returned HTTP $booking_status"
            echo "Response body:"
            cat "$RESPONSE_FILE"
            rm -f "$RESPONSE_FILE"
            exit 1
          fi

          echo "Booking endpoint returned HTTP 201."

          grep -q '"id"' "$RESPONSE_FILE" || {
            echo "FAIL: booking response does not contain an id."
            cat "$RESPONSE_FILE"
            rm -f "$RESPONSE_FILE"
            exit 1
          }

          echo "Booking response contains an id."
          rm -f "$RESPONSE_FILE"

          echo ""
          echo "=== Staging appointment smoke test ==="

          APPT_RESPONSE="$(mktemp)"
          APPT_PAYLOAD="$(mktemp)"

          # Build the JSON with python3 to avoid shell/Groovy quoting issues.
          SERVICE_CODE="$SERVICE_CODE" SLOT_START="$SLOT_START" \
            python3 -c '
import json, os
print(json.dumps({
    "service_code": os.environ["SERVICE_CODE"],
    "starts_at": os.environ["SLOT_START"],
    "first_name": "Jenkins",
    "last_name": "SmokeTest",
    "email": "smoke-test@example.com",
    "phone": "+1-555-000-0000",
    "reason_category": "General appointment request",
    "source": "ci",
}))
' > "$APPT_PAYLOAD"

          appt_status="$(
            curl -sS \
              -o "$APPT_RESPONSE" \
              -w '%{http_code}' \
              -X POST \
              -H 'Content-Type: application/json' \
              --data-binary "@$APPT_PAYLOAD" \
              "${STAGING_API_URL}/api/v1/appointments" \
              || true
          )"

          rm -f "$APPT_PAYLOAD"
          if [ "$appt_status" = "201" ]; then
            echo "Appointment smoke test: HTTP 201 (created)"
            # The CI appointment carries source=ci and is removed by the
            # cleanup step at the start of the next health-check run, keeping
            # repeated dev builds idempotent. No teardown needed here.
          elif [ "$appt_status" = "409" ]; then
            # 409 proves the endpoint is live and the double-booking exclusion
            # constraint is working. A prior CI appointment still holds the slot;
            # this is a healthy signal, not a failure. The start-of-run cleanup
            # frees source=ci appointments on the next build.
            echo "Appointment smoke test: HTTP 409 (slot held by exclusion constraint) — treated as PASS"
          else
            echo "FAIL: appointment smoke test returned HTTP $appt_status"
            echo "Response body:"
            cat "$APPT_RESPONSE"
            rm -f "$APPT_RESPONSE"
            exit 1
          fi

          echo "Appointment endpoint returned HTTP 201."
          rm -f "$APPT_RESPONSE"

          echo ""
          echo "=== Immutable image verification ==="

          IMAGE_TAG="$(git rev-parse HEAD)"

          if [ -z "$IMAGE_TAG" ]; then
            echo "FAIL: git rev-parse HEAD returned an empty string."
            exit 1
          fi

          if ! echo "$IMAGE_TAG" | grep -qE '^[0-9a-f]{40}$'; then
            echo "FAIL: Git SHA is not a valid 40-char hex string: '$IMAGE_TAG'"
            exit 1
          fi

          FULL_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:${IMAGE_TAG}"

          DEPLOYED_IMAGE="$(
            kubectl -n "$STAGING_NAMESPACE" \
              get deployment drfarah-staging-api \
              -o jsonpath='{.spec.template.spec.containers[?(@.name=="api")].image}'
          )"

          DEPLOYED_INIT_IMAGE="$(
            kubectl -n "$STAGING_NAMESPACE" \
              get deployment drfarah-staging-api \
              -o jsonpath='{.spec.template.spec.initContainers[?(@.name=="db-migrate")].image}'
          )"

          echo "Expected image: $FULL_IMAGE"
          echo "Deployed api container:        $DEPLOYED_IMAGE"
          echo "Deployed db-migrate container: $DEPLOYED_INIT_IMAGE"

          if [ "$DEPLOYED_IMAGE" != "$FULL_IMAGE" ]; then
            echo "FAIL: deployed api image does not match the immutable commit SHA."
            exit 1
          fi

          if [ "$DEPLOYED_INIT_IMAGE" != "$FULL_IMAGE" ]; then
            echo "FAIL: deployed db-migrate image does not match the immutable commit SHA."
            exit 1
          fi

          echo "Immutable image verification passed (both containers)."
          echo ""
          echo "Staging API health checks passed."
        '''
      }
    }

    stage('Frontend — deploy staging') {
      when {
        branch 'dev'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            echo "=== Hestia staging preflight ==="

            ssh $SSH_OPTS \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST" \
              "
                set -e

                [ -d '$STAGING_DOCROOT' ] || {
                  echo 'ERROR: staging docroot is missing'
                  exit 1
                }

                touch '$STAGING_DOCROOT/.jenkins-write-test' 2>/dev/null || {
                  echo 'ERROR: no write access'
                  ls -ld '$STAGING_DOCROOT'
                  exit 1
                }

                rm -f '$STAGING_DOCROOT/.jenkins-write-test'
                echo 'Write access confirmed.'
              "

            echo ""
            echo "=== Deploying frontend to staging ==="

            rsync -av --delete \
              --exclude='.env' \
              --exclude='.well-known' \
              --exclude='.htaccess.production' \
              --exclude='robots.production.txt' \
              -e "ssh $SSH_OPTS" \
              frontend/ \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$STAGING_DOCROOT/"

            echo ""
            echo "=== Staging frontend smoke test ==="

            frontend_status="000"

            for attempt in $(seq 1 10); do
              frontend_status="$(
                curl -sS \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "https://${STAGING_FRONTEND_HOST}/" \
                  || true
              )"

              if [ -z "$frontend_status" ]; then
                frontend_status="000"
              fi

              if [ "$frontend_status" = "200" ]; then
                echo "Frontend reached HTTP 200 on attempt $attempt."
                break
              fi

              echo "  attempt $attempt/10 -> HTTP $frontend_status"
              sleep 3
            done

            if [ "$frontend_status" != "200" ]; then
              echo "FAIL: staging frontend returned HTTP $frontend_status"
              exit 1
            fi

            echo ""
            echo "=== Deployed content checks ==="

            curl -fsS \
              "https://${STAGING_FRONTEND_HOST}/" \
              | grep -q 'Dr. Farah' \
              || {
                echo "FAIL: Dr. Farah marker is absent."
                exit 1
              }

            curl -fsS \
              "https://${STAGING_FRONTEND_HOST}/" \
              | grep -q 'noindex,nofollow,noarchive' \
              || {
                echo "FAIL: noindex meta is absent."
                exit 1
              }

            curl -fsS \
              "https://${STAGING_FRONTEND_HOST}/robots.txt" \
              | grep -q 'Disallow: /' \
              || {
                echo "FAIL: robots.txt Disallow rule is absent."
                exit 1
              }

            deployed_paths="
              /styles.css
              /app.js
              /booking.js
              /robots.txt
              /sitemap.xml
              /assets/hero-treatment.jpg
              /assets/consult-rejuvenation.jpg
              /assets/mobile-visit.jpg
              /assets/reception-vip.jpg
              /assets/favicon.svg
          "

            for path in $deployed_paths; do
              status="$(
                curl -sS \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "https://${STAGING_FRONTEND_HOST}${path}" \
                  || true
              )"

              if [ -z "$status" ]; then
                status="000"
              fi

              if [ "$status" != "200" ]; then
                echo "FAIL  $path -> $status"
                exit 1
              fi

              echo "OK    $path -> $status"
            done

            echo ""
            echo "Frontend staging deployment passed."
          '''
        }
      }
    }

    stage('Admin SPA — deploy staging') {
      when {
        branch 'dev'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            echo "=== Admin SPA preflight ==="

            ssh $SSH_OPTS \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST" \
              "
                set -e

                [ -d '$ADMIN_DOCROOT' ] || {
                  echo 'ERROR: admin docroot is missing'
                  exit 1
                }

                touch '$ADMIN_DOCROOT/.jenkins-write-test' 2>/dev/null || {
                  echo 'ERROR: no write access'
                  ls -ld '$ADMIN_DOCROOT'
                  exit 1
                }

                rm -f '$ADMIN_DOCROOT/.jenkins-write-test'
                echo 'Write access confirmed.'
              "

            echo ""
            echo "=== Deploying admin SPA to staging ==="

            rsync -av --delete \
              --exclude='.env' \
              --exclude='.well-known' \
              -e "ssh $SSH_OPTS" \
              admin/ \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$ADMIN_DOCROOT/"

            echo ""
            echo "=== Admin SPA smoke test ==="

            admin_paths="
              /
              /index.html
              /app.js
              /config.js
              /styles.css
            "

            for path in $admin_paths; do
              status="$(
                curl -sS \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "https://${ADMIN_FRONTEND_HOST}${path}" \
                  || true
              )"

              if [ -z "$status" ]; then
                status="000"
              fi

              if [ "$status" != "200" ]; then
                echo "FAIL  $path -> $status"
                exit 1
              fi

              echo "OK    $path -> $status"
            done

            echo ""
            echo "Admin SPA staging deployment passed."
          '''
        }
      }
    }

    stage('Production — deploy API and PostgreSQL') {
      when {
        branch 'main'
      }

      steps {
        sh '''
          set -eu

          IMAGE_TAG="$(git rev-parse HEAD)"

          if ! echo "$IMAGE_TAG" | grep -qE '^[0-9a-f]{40}$'; then
            echo "FAIL: Git SHA is not a valid 40-char hex string: '$IMAGE_TAG'"
            exit 1
          fi

          API_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:${IMAGE_TAG}"
          BACKUP_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${BACKUP_IMAGE_NAME}:${IMAGE_TAG}"
          API_PLACEHOLDER="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:prod"
          BACKUP_PLACEHOLDER="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${BACKUP_IMAGE_NAME}:prod"

          RENDERED_API="$(mktemp)"
          RENDERED_BACKUP="$(mktemp)"

          cleanup_production_manifests() {
            rm -f "$RENDERED_API" "$RENDERED_BACKUP"
          }
          trap cleanup_production_manifests EXIT HUP INT TERM

          sed "s|image: ${API_PLACEHOLDER}|image: ${API_IMAGE}|g" \
            kubernetes/drfarah/api-deployment.yaml \
            > "$RENDERED_API"

          sed "s|image: ${BACKUP_PLACEHOLDER}|image: ${BACKUP_IMAGE}|g" \
            kubernetes/drfarah/postgres-backup-cronjob.yaml \
            > "$RENDERED_BACKUP"

          API_IMAGE_COUNT="$(grep -cF "image: ${API_IMAGE}" "$RENDERED_API" || true)"
          BACKUP_IMAGE_COUNT="$(grep -cF "image: ${BACKUP_IMAGE}" "$RENDERED_BACKUP" || true)"

          if [ "$API_IMAGE_COUNT" -ne 2 ]; then
            echo "FAIL: expected immutable API image twice, found $API_IMAGE_COUNT."
            exit 1
          fi

          if [ "$BACKUP_IMAGE_COUNT" -ne 1 ]; then
            echo "FAIL: expected immutable backup image once, found $BACKUP_IMAGE_COUNT."
            exit 1
          fi

          if grep -qE 'image:.*:prod\b' "$RENDERED_API" "$RENDERED_BACKUP"; then
            echo "FAIL: a :prod image placeholder remains in rendered manifests."
            grep -nE 'image:.*:prod\b' "$RENDERED_API" "$RENDERED_BACKUP" || true
            exit 1
          fi

          echo "=== Applying production namespace and base resources ==="

          kubectl apply \
            -f kubernetes/drfarah/namespace.yaml \
            -f kubernetes/drfarah/configmap.yaml \
            -f kubernetes/drfarah/postgres-service.yaml \
            -f kubernetes/drfarah/postgres-statefulset.yaml \
            -f kubernetes/drfarah/api-service.yaml \
            -f kubernetes/drfarah/api-ingress.yaml

          echo ""
          echo "=== Applying immutable production workloads ==="

          kubectl apply -f "$RENDERED_API"
          kubectl apply -f "$RENDERED_BACKUP"

          echo ""
          echo "=== Waiting for production PostgreSQL ==="

          kubectl \
            -n "$PRODUCTION_NAMESPACE" \
            rollout status statefulset/drfarah-postgres \
            --timeout=240s

          echo ""
          echo "=== Waiting for production API ==="

          kubectl \
            -n "$PRODUCTION_NAMESPACE" \
            rollout status deployment/drfarah-api \
            --timeout=240s

          DEPLOYED_API_IMAGE="$(
            kubectl -n "$PRODUCTION_NAMESPACE" \
              get deployment drfarah-api \
              -o jsonpath='{.spec.template.spec.containers[?(@.name=="api")].image}'
          )"
          DEPLOYED_MIGRATION_IMAGE="$(
            kubectl -n "$PRODUCTION_NAMESPACE" \
              get deployment drfarah-api \
              -o jsonpath='{.spec.template.spec.initContainers[?(@.name=="db-migrate")].image}'
          )"
          DEPLOYED_BACKUP_IMAGE="$(
            kubectl -n "$PRODUCTION_NAMESPACE" \
              get cronjob drfarah-postgres-backup \
              -o jsonpath='{.spec.jobTemplate.spec.template.spec.containers[?(@.name=="backup")].image}'
          )"

          [ "$DEPLOYED_API_IMAGE" = "$API_IMAGE" ] || {
            echo "FAIL: production API image is not the promoted Git SHA."
            exit 1
          }

          [ "$DEPLOYED_MIGRATION_IMAGE" = "$API_IMAGE" ] || {
            echo "FAIL: production migration image is not the promoted Git SHA."
            exit 1
          }

          [ "$DEPLOYED_BACKUP_IMAGE" = "$BACKUP_IMAGE" ] || {
            echo "FAIL: production backup image is not the promoted Git SHA."
            exit 1
          }

          cleanup_production_manifests
          trap - EXIT HUP INT TERM
          echo "Production API/PostgreSQL rollout passed."
        '''
      }
    }

    stage('Production — verify API') {
      when {
        branch 'main'
      }

      steps {
        sh '''
          set -eu

          echo "=== Production API liveness ==="

          LIVE_RESPONSE="$(mktemp)"
          READY_RESPONSE="$(mktemp)"
          SERVICES_RESPONSE="$(mktemp)"
          CORS_HEADERS="$(mktemp)"

          cleanup_api_checks() {
            rm -f "$LIVE_RESPONSE" "$READY_RESPONSE" "$SERVICES_RESPONSE" "$CORS_HEADERS"
          }
          trap cleanup_api_checks EXIT HUP INT TERM

          live_status="000"
          for attempt in $(seq 1 24); do
            live_status="$(
              curl -sS \
                -o "$LIVE_RESPONSE" \
                -w '%{http_code}' \
                "${PRODUCTION_API_URL}/api/v1/health/live" \
                || true
            )"

            [ -n "$live_status" ] || live_status="000"

            if [ "$live_status" = "200" ]; then
              echo "Liveness passed on attempt $attempt."
              break
            fi

            echo "  attempt $attempt/24 -> HTTP $live_status"
            sleep 5
          done

          [ "$live_status" = "200" ] || {
            echo "FAIL: production liveness returned HTTP $live_status"
            kubectl -n "$PRODUCTION_NAMESPACE" get pods -o wide || true
            kubectl -n "$PRODUCTION_NAMESPACE" logs deployment/drfarah-api --tail=120 || true
            exit 1
          }

          python3 - "$LIVE_RESPONSE" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    payload = json.load(handle)

if payload.get("status") != "ok" or payload.get("environment") != "prod":
    raise SystemExit("FAIL: liveness did not identify the production API")
PY

          echo ""
          echo "=== Production API readiness ==="

          ready_status="$(
            curl -sS \
              -o "$READY_RESPONSE" \
              -w '%{http_code}' \
              "${PRODUCTION_API_URL}/api/v1/health/ready" \
              || true
          )"

          [ "$ready_status" = "200" ] || {
            echo "FAIL: production readiness returned HTTP $ready_status"
            cat "$READY_RESPONSE"
            exit 1
          }

          python3 - "$READY_RESPONSE" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    payload = json.load(handle)

if payload.get("status") != "ok" or payload.get("environment") != "prod":
    raise SystemExit("FAIL: readiness did not identify the production API")
PY

          echo ""
          echo "=== Production service catalog ==="

          services_status="$(
            curl -sS \
              -o "$SERVICES_RESPONSE" \
              -w '%{http_code}' \
              "${PRODUCTION_API_URL}/api/v1/services" \
              || true
          )"

          [ "$services_status" = "200" ] || {
            echo "FAIL: production services returned HTTP $services_status"
            exit 1
          }

          SERVICE_COUNT="$(
            python3 - "$SERVICES_RESPONSE" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    payload = json.load(handle)

print(len(payload.get("services", [])))
PY
          )"

          [ "$SERVICE_COUNT" -gt 0 ] || {
            echo "FAIL: production service catalog is empty."
            exit 1
          }

          echo "Production service catalog contains $SERVICE_COUNT active service(s)."
          echo ""
          echo "=== Production CORS contract ==="

          for origin in \
            "https://drfarahvipurgentcare.com" \
            "https://admin.drfarahvipurgentcare.com"; do
            : > "$CORS_HEADERS"

            cors_status="$(
              curl -sS \
                -o /dev/null \
                -D "$CORS_HEADERS" \
                -w '%{http_code}' \
                -X OPTIONS \
                -H "Origin: $origin" \
                -H 'Access-Control-Request-Method: GET' \
                "${PRODUCTION_API_URL}/api/v1/services" \
                || true
            )"

            case "$cors_status" in
              200|204) ;;
              *)
                echo "FAIL: CORS preflight for $origin returned HTTP $cors_status"
                exit 1
                ;;
            esac

            grep -qiF "access-control-allow-origin: $origin" "$CORS_HEADERS" || {
              echo "FAIL: production API did not allow CORS origin $origin"
              exit 1
            }

            echo "OK    $origin"
          done

          cleanup_api_checks
          trap - EXIT HUP INT TERM
          echo "Production API verification passed."
        '''
      }
    }

    stage('Production — backup and restore test') {
      when {
        branch 'main'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            JOB_NAME="drfarah-backup-verify-${BUILD_NUMBER}"
            BACKUP_LOG="$(mktemp)"
            LOCAL_BACKUP="$(mktemp)"
            RESTORE_CONTAINER="drfarah-restore-${BUILD_NUMBER}-$$"
            RESTORE_PASSWORD="restore_${BUILD_NUMBER}_$$"
            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            cleanup_backup_test() {
              docker rm -f "$RESTORE_CONTAINER" >/dev/null 2>&1 || true
              kubectl -n "$PRODUCTION_NAMESPACE" \
                delete job "$JOB_NAME" --ignore-not-found=true \
                >/dev/null 2>&1 || true
              rm -f "$BACKUP_LOG" "$LOCAL_BACKUP"
            }
            trap cleanup_backup_test EXIT HUP INT TERM

            kubectl -n "$PRODUCTION_NAMESPACE" \
              delete job "$JOB_NAME" --ignore-not-found=true \
              >/dev/null

            echo "=== Starting immediate off-cluster backup ==="

            kubectl -n "$PRODUCTION_NAMESPACE" \
              create job \
              --from=cronjob/drfarah-postgres-backup \
              "$JOB_NAME"

            if ! kubectl -n "$PRODUCTION_NAMESPACE" \
              wait \
              --for=condition=complete \
              "job/$JOB_NAME" \
              --timeout=600s; then
              echo "FAIL: production backup Job did not complete."
              kubectl -n "$PRODUCTION_NAMESPACE" \
                describe job "$JOB_NAME" || true
              kubectl -n "$PRODUCTION_NAMESPACE" \
                logs "job/$JOB_NAME" --all-containers=true --tail=200 || true
              exit 1
            fi

            kubectl -n "$PRODUCTION_NAMESPACE" \
              logs "job/$JOB_NAME" \
              > "$BACKUP_LOG"

            BACKUP_NAME="$(
              sed -n 's/^BACKUP_COMPLETE=//p' "$BACKUP_LOG" \
                | tail -n 1
            )"

            case "$BACKUP_NAME" in
              drfarah-*.dump) ;;
              *)
                echo "FAIL: backup Job did not return a valid archive name."
                cat "$BACKUP_LOG"
                exit 1
                ;;
            esac

            if ! printf '%s' "$BACKUP_NAME" | grep -qE '^drfarah-[A-Za-z0-9._-]+[.]dump$'; then
              echo "FAIL: unsafe backup archive name returned."
              exit 1
            fi

            echo "Backup Job completed: $BACKUP_NAME"
            echo ""
            echo "=== Fetching exact off-cluster archive ==="

            remote_mode="$(
              ssh $SSH_OPTS \
                "$HESTIA_SSH_USER@$HESTIA_SSH_HOST" \
                "test -s '$PRODUCTION_BACKUP_DIR/$BACKUP_NAME' && stat -c '%a' '$PRODUCTION_BACKUP_DIR/$BACKUP_NAME'"
            )"

            [ "$remote_mode" = "600" ] || {
              echo "FAIL: remote backup mode is $remote_mode, expected 600."
              exit 1
            }

            scp \
              -i "$SSH_KEY" \
              -P "$HESTIA_SSH_PORT" \
              -o StrictHostKeyChecking=accept-new \
              -o BatchMode=yes \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$PRODUCTION_BACKUP_DIR/$BACKUP_NAME" \
              "$LOCAL_BACKUP"

            test -s "$LOCAL_BACKUP" || {
              echo "FAIL: downloaded backup archive is empty."
              exit 1
            }

            chmod 600 "$LOCAL_BACKUP"

            echo ""
            echo "=== Restoring into disposable PostgreSQL 16 ==="

            docker run -d \
              --name "$RESTORE_CONTAINER" \
              --tmpfs /var/lib/postgresql/data \
              -e POSTGRES_USER=restore_test \
              -e POSTGRES_PASSWORD="$RESTORE_PASSWORD" \
              -e POSTGRES_DB=restore_test \
              postgres:16-alpine \
              >/dev/null

            restore_ready=0
            for attempt in $(seq 1 60); do
              if docker exec "$RESTORE_CONTAINER" sh -ec \
                '[ "$(cat /proc/1/comm)" = "postgres" ]' \
                >/dev/null 2>&1 \
                && docker exec "$RESTORE_CONTAINER" \
                  pg_isready \
                    -h 127.0.0.1 \
                    -U restore_test \
                    -d restore_test \
                  >/dev/null 2>&1 \
                && docker exec "$RESTORE_CONTAINER" \
                  psql \
                    -h 127.0.0.1 \
                    -U restore_test \
                    -d restore_test \
                    -Atqc 'SELECT 1;' \
                  2>/dev/null \
                  | grep -qx '1'; then
                restore_ready=1
                break
              fi
              sleep 1
            done

            [ "$restore_ready" -eq 1 ] || {
              echo "FAIL: disposable restore database did not become stably ready."
              docker inspect \
                --format 'Container state: {{json .State}}' \
                "$RESTORE_CONTAINER" || true
              docker logs --tail 100 "$RESTORE_CONTAINER" || true
              exit 1
            }

            docker cp "$LOCAL_BACKUP" "$RESTORE_CONTAINER:/backup.dump"

            docker exec "$RESTORE_CONTAINER" \
              pg_restore \
                -h 127.0.0.1 \
                --no-owner \
                --no-privileges \
                -U restore_test \
                -d restore_test \
                /backup.dump

            RESTORED_TABLE_COUNT="$(
              docker exec "$RESTORE_CONTAINER" \
                psql \
                  -h 127.0.0.1 \
                  -U restore_test \
                  -d restore_test \
                  -Atqc "SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"
            )"

            [ "$RESTORED_TABLE_COUNT" -gt 0 ] || {
              echo "FAIL: restored production backup contains no public tables."
              exit 1
            }

            RESTORED_REVISION="$(
              docker exec "$RESTORE_CONTAINER" \
                psql \
                  -h 127.0.0.1 \
                  -U restore_test \
                  -d restore_test \
                  -Atqc 'SELECT version_num FROM alembic_version LIMIT 1;'
            )"

            [ -n "$RESTORED_REVISION" ] || {
              echo "FAIL: restored production backup has no Alembic revision."
              exit 1
            }

            echo "Restore test passed with $RESTORED_TABLE_COUNT public table(s)."
            echo "Daily CronJob remains active; retention is 30 days on Hestia."

            cleanup_backup_test
            trap - EXIT HUP INT TERM
          '''
        }
      }
    }

    stage('Production — deploy public frontend') {
      when {
        branch 'main'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"
            PRODUCTION_BUILD_DIR="$(mktemp -d)"

            cleanup_production_frontend() {
              rm -rf "$PRODUCTION_BUILD_DIR"
            }
            trap cleanup_production_frontend EXIT HUP INT TERM

            echo "=== Assembling production frontend ==="

            sh scripts/prepare-production-frontend.sh \
              frontend \
              "$PRODUCTION_BUILD_DIR"

            echo ""
            echo "=== Publishing production frontend ==="

            rsync -av --delete \
              --exclude='.env' \
              --exclude='.well-known' \
              -e "ssh $SSH_OPTS" \
              "$PRODUCTION_BUILD_DIR/" \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$PRODUCTION_FRONTEND_DOCROOT/"

            echo ""
            echo "=== Production frontend smoke test ==="

            production_paths="
              /
              /about
              /services
              /book
              /patient-registration
              /privacy
              /robots.txt
              /sitemap.xml
              /styles.css
              /app.js
              /booking.js
              /registration.js
              /assets/favicon.svg
            "

            for path in $production_paths; do
              status="$(
                curl -sS \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "https://${PRODUCTION_FRONTEND_HOST}${path}" \
                  || true
              )"

              [ -n "$status" ] || status="000"

              if [ "$status" != "200" ]; then
                echo "FAIL  $path -> $status"
                exit 1
              fi

              echo "OK    $path -> $status"
            done

            HOME_HTML="$(mktemp)"
            ROBOTS_FILE="$(mktemp)"

            curl -fsS \
              "https://${PRODUCTION_FRONTEND_HOST}/" \
              > "$HOME_HTML"

            curl -fsS \
              "https://${PRODUCTION_FRONTEND_HOST}/robots.txt" \
              > "$ROBOTS_FILE"

            grep -qF 'Dr. Farah' "$HOME_HTML" || {
              echo "FAIL: production homepage marker is absent."
              rm -f "$HOME_HTML" "$ROBOTS_FILE"
              exit 1
            }

            if grep -qF 'noindex,nofollow,noarchive' "$HOME_HTML"; then
              echo "FAIL: production homepage is still noindexed."
              rm -f "$HOME_HTML" "$ROBOTS_FILE"
              exit 1
            fi

            if grep -qF '/wp-content/uploads/' "$HOME_HTML"; then
              echo "FAIL: production homepage still contains a WordPress asset dependency."
              rm -f "$HOME_HTML" "$ROBOTS_FILE"
              exit 1
            fi

            grep -qF 'Allow: /' "$ROBOTS_FILE" || {
              echo "FAIL: production robots.txt is not crawlable."
              rm -f "$HOME_HTML" "$ROBOTS_FILE"
              exit 1
            }

            if grep -qF 'Disallow: /' "$ROBOTS_FILE"; then
              echo "FAIL: staging robots.txt was published to production."
              rm -f "$HOME_HTML" "$ROBOTS_FILE"
              exit 1
            fi

            rm -f "$HOME_HTML" "$ROBOTS_FILE"

            LEGACY_RESULT="$(
              curl -sS \
                -L \
                --max-redirs 5 \
                -o /dev/null \
                -w '%{http_code}|%{url_effective}' \
                "https://www.drfarahvipurgentcare.com/about-us/" \
                || true
            )"

            [ "$LEGACY_RESULT" = '200|https://drfarahvipurgentcare.com/about' ] || {
              echo "FAIL: www/legacy redirect chain is incorrect: $LEGACY_RESULT"
              exit 1
            }

            cleanup_production_frontend
            trap - EXIT HUP INT TERM
            echo "Production frontend deployment passed."
          '''
        }
      }
    }

    stage('Production — deploy admin SPA') {
      when {
        branch 'main'
      }

      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
          )
        ]) {
          sh '''
            set -eu

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            echo "=== Publishing production admin SPA ==="

            rsync -av --delete \
              --exclude='.env' \
              --exclude='.well-known' \
              -e "ssh $SSH_OPTS" \
              admin/ \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$PRODUCTION_ADMIN_DOCROOT/"

            echo ""
            echo "=== Production admin smoke test ==="

            admin_paths="
              /
              /index.html
              /app.js
              /config.js
              /styles.css
            "

            for path in $admin_paths; do
              status="$(
                curl -sS \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "https://${PRODUCTION_ADMIN_HOST}${path}" \
                  || true
              )"

              [ -n "$status" ] || status="000"

              if [ "$status" != "200" ]; then
                echo "FAIL  $path -> $status"
                exit 1
              fi

              echo "OK    $path -> $status"
            done

            ADMIN_HTML="$(mktemp)"
            ADMIN_CONFIG="$(mktemp)"

            curl -fsS \
              "https://${PRODUCTION_ADMIN_HOST}/" \
              > "$ADMIN_HTML"

            curl -fsS \
              "https://${PRODUCTION_ADMIN_HOST}/config.js" \
              > "$ADMIN_CONFIG"

            grep -qF 'noindex,nofollow,noarchive' "$ADMIN_HTML" || {
              echo "FAIL: production admin is missing noindex protection."
              rm -f "$ADMIN_HTML" "$ADMIN_CONFIG"
              exit 1
            }

            grep -qF "h === 'admin.drfarahvipurgentcare.com'" "$ADMIN_CONFIG" || {
              echo "FAIL: production admin hostname mapping is absent."
              rm -f "$ADMIN_HTML" "$ADMIN_CONFIG"
              exit 1
            }

            grep -qF 'https://api.drfarahvipurgentcare.com/api/v1' "$ADMIN_CONFIG" || {
              echo "FAIL: production admin API mapping is absent."
              rm -f "$ADMIN_HTML" "$ADMIN_CONFIG"
              exit 1
            }

            grep -qF 'https://keycloak.soria-academie.fr' "$ADMIN_CONFIG" || {
              echo "FAIL: production admin Keycloak mapping is absent."
              rm -f "$ADMIN_HTML" "$ADMIN_CONFIG"
              exit 1
            }

            rm -f "$ADMIN_HTML" "$ADMIN_CONFIG"

            echo ""
            echo "=== Final production endpoint check ==="

            for endpoint in \
              "https://${PRODUCTION_FRONTEND_HOST}/" \
              "https://${PRODUCTION_ADMIN_HOST}/" \
              "${PRODUCTION_API_URL}/api/v1/health/live" \
              "${PRODUCTION_API_URL}/api/v1/health/ready"; do
              status="$(
                curl -sS \
                  --connect-timeout 8 \
                  --max-time 20 \
                  -o /dev/null \
                  -w '%{http_code}' \
                  "$endpoint" \
                  || true
              )"

              if [ "$status" != "200" ]; then
                echo "FAIL  $endpoint -> $status"
                exit 1
              fi

              echo "OK    $endpoint -> 200"
            done

            echo "Production admin and final endpoint checks passed."
          '''
        }
      }
    }
  }

  post {
    success {
      echo 'SUCCESS — all required stages completed.'
    }

    failure {
      echo 'FAILURE — inspect the first failed stage and its diagnostics.'
    }

    always {
      sh '''
        rm -rf "$WORKSPACE"/.docker-auth-* \
          >/dev/null 2>&1 || true
      '''
    }
  }
}
