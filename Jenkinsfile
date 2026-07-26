pipeline {
  agent any

  options {
    timestamps()
    skipDefaultCheckout(true)
    disableConcurrentBuilds()
  }

  environment {
    PROJECT_SLUG      = 'drfarah'

    HARBOR_REGISTRY   = 'harbor.proxbenovh.cloud'
    HARBOR_PROJECT    = 'devops-project-harbor'
    API_IMAGE_NAME    = 'drfarah-api'

    KUBECONFIG        = '/var/lib/jenkins/.kube/config-afpa-k3s'
    STAGING_NAMESPACE = 'drfarah-staging'
    STAGING_API_URL   = 'https://api.staging.drfarah.proxbenovh.cloud'

    HESTIA_SSH_HOST   = '192.168.100.75'
    HESTIA_SSH_PORT   = '2275'
    HESTIA_SSH_USER   = 'benweb'
    STAGING_FRONTEND_HOST = 'staging.drfarah.proxbenovh.cloud'
    STAGING_DOCROOT   = '/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html'
  }

  // =========================================================================
  // JENKINSFILE — Phase 1
  //
  // All branches:
  //   - Clean checkout
  //   - Repository and secret-filename checks
  //   - Markdown inventory
  //   - API tests in an isolated Python container
  //   - Production API image build/runtime validation
  //   - Frontend syntax and static-serving validation
  //
  // dev only:
  //   - Build and push API image to Harbor
  //   - Apply/update staging Kubernetes resources
  //   - Verify staging API and booking endpoint
  //   - Deploy frontend to staging Hestia docroot
  //
  // main:
  //   - Validation only. Production deployment is intentionally disabled.
  //
  // Hard rules:
  //   - No secrets in Git or logs
  //   - No manual deployment
  //   - No production deployment in this phase
  //   - Jenkins kubeconfig is a file on the agent, not a Jenkins credential
  //   - Docker authentication is isolated per build
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
            admin/README.md
            api/README.md
            api/Dockerfile
            api/requirements.txt
            api/requirements-dev.txt
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
            kubernetes/drfarah/README.md
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

    stage('Detect committed secret filenames') {
      steps {
        sh '''
          set -eu

          hits="$(
            find . \
              \( \
                -name '.env' \
                -o -name 'secret.yaml' \
                -o -name 'secrets.yaml' \
                -o -name '*.tfstate' \
                -o -name '*.tfvars' \
                -o -name 'credentials.json' \
                -o -name 'service-account-key.json' \
                -o -name 'id_rsa' \
                -o -name 'id_ed25519' \
                -o -name '*.pem' \
              \) \
              -not -name '*.example' \
              -not -path './.git/*' \
              -print
          )"

          if [ -n "$hits" ]; then
            echo "FAIL: forbidden secret filenames found:"
            echo "$hits"
            exit 1
          fi

          echo "OK: no forbidden secret filenames detected."
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
              -w /app \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/drfarah-ci.db' \
              -e PYTHONDONTWRITEBYTECODE=1 \
              -e PYTHONPYCACHEPREFIX=/tmp/pycache \
              python:3.12-slim \
              bash -c '
                set -e
                rm -f /tmp/drfarah-ci.db
                pip install -q -r requirements.txt -r requirements-dev.txt
                PYTHONPATH=. python -m pytest -q -p no:cacheprovider tests/
              '

            echo "API tests passed."
          '''
        }
      }
    }

    stage('API — Docker build validation') {
      steps {
        dir('api') {
          sh '''
            set -eu

            CONTAINER_NAME="drfarah-api-validation-${BUILD_NUMBER}"
            IMAGE_NAME="drfarah-api:test-build"

            cleanup() {
              docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
              docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true
            }
            trap cleanup EXIT HUP INT TERM

            echo "=== Building production API image ==="
            docker build -t "$IMAGE_NAME" .
            echo "Docker image build passed."

            docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

            echo ""
            echo "=== Starting isolated validation container ==="
            docker run -d \
              --name "$CONTAINER_NAME" \
              -P \
              -e ENVIRONMENT=test \
              -e DATABASE_URL='sqlite:////tmp/drfarah-validation.db' \
              "$IMAGE_NAME" >/dev/null

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
              echo "FAIL: Docker did not publish the validation port."
              docker ps -a --filter "name=$CONTAINER_NAME" || true
              docker inspect "$CONTAINER_NAME" \
                --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
                || true
              docker logs --tail 200 "$CONTAINER_NAME" || true
              exit 1
            fi

            echo "Published validation port: $HOST_PORT"
            echo ""
            echo "=== Waiting for liveness endpoint ==="

            healthy=0

            for attempt in $(seq 1 30); do
              state="$(
                docker inspect "$CONTAINER_NAME" \
                  --format '{{.State.Status}}' 2>/dev/null \
                  || echo missing
              )"

              if [ "$state" = "exited" ] || [ "$state" = "dead" ] || [ "$state" = "missing" ]; then
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
              docker ps -a --filter "name=$CONTAINER_NAME" || true

              echo ""
              echo "--- container state ---"
              docker inspect "$CONTAINER_NAME" \
                --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \
                || true

              echo ""
              echo "--- container logs (last 200 lines) ---"
              docker logs --tail 200 "$CONTAINER_NAME" || true
              exit 1
            fi

            echo ""
            echo "=== Liveness response ==="
            curl -fsS "http://127.0.0.1:${HOST_PORT}/api/v1/health/live"
            echo ""

            echo ""
            echo "=== Readiness response ==="
            curl -fsS "http://127.0.0.1:${HOST_PORT}/api/v1/health/ready"
            echo ""

            echo ""
            echo "API Docker runtime validation passed."
          '''
        }
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
            node --check frontend/app.js

          echo "JavaScript syntax passed."

          echo ""
          echo "=== Temporary-domain indexing protection ==="

          grep -q 'noindex,nofollow,noarchive' frontend/index.html || {
            echo "FAIL: noindex meta is missing."
            exit 1
          }

          grep -q 'Disallow: /' frontend/robots.txt || {
            echo "FAIL: robots.txt Disallow rule is missing."
            exit 1
          }

          echo "No-index checks passed."

          echo ""
          echo "=== Static frontend serving validation ==="

          CONTAINER_NAME="drfarah-frontend-validation-${BUILD_NUMBER}"

          cleanup_frontend() {
            docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
          }
          trap cleanup_frontend EXIT HUP INT TERM

          docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

          docker run -d \
            --name "$CONTAINER_NAME" \
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

            sleep 1
          done

          if [ -z "$HOST_PORT" ]; then
            echo "FAIL: frontend validation port was not published."
            docker logs --tail 100 "$CONTAINER_NAME" || true
            exit 1
          fi

          server_ready=0

          for attempt in $(seq 1 15); do
            if curl -fsS "http://127.0.0.1:${HOST_PORT}/" >/dev/null 2>&1; then
              server_ready=1
              break
            fi
            sleep 1
          done

          if [ "$server_ready" -ne 1 ]; then
            echo "FAIL: frontend static server did not become ready."
            docker ps -a --filter "name=$CONTAINER_NAME" || true
            docker logs --tail 100 "$CONTAINER_NAME" || true
            exit 1
          fi

          public_paths="
            /
            /styles.css
            /app.js
            /robots.txt
            /assets/logo-mark.svg
            /assets/favicon.svg
            /assets/doctor-portrait.svg
            /assets/hero-clinic.svg
            /assets/urgent-care.svg
            /assets/mobile-care.svg
            /assets/traveler-care.svg
            /assets/rejuvenation-main.svg
            /assets/clinic-map.svg
            /assets/og-preview.svg
          "

          for path in $public_paths; do
            status="$(
              curl -sS -o /dev/null -w '%{http_code}' \
                "http://127.0.0.1:${HOST_PORT}${path}"
            )"

            if [ "$status" != "200" ]; then
              echo "FAIL  $path -> $status"
              exit 1
            fi

            echo "OK    $path -> $status"
          done

          echo ""
          echo "Frontend validation passed."
        '''
      }
    }

    stage('API — build and push to Harbor') {
      when {
        branch 'dev'
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

            IMAGE_TAG="${GIT_COMMIT:-dev}"
            FULL_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}"
            BUILD_IMAGE="${FULL_IMAGE}:${IMAGE_TAG}"
            DEV_IMAGE="${FULL_IMAGE}:dev"

            DOCKER_CONFIG="${WORKSPACE}/.docker-auth-${BUILD_NUMBER}"
            export DOCKER_CONFIG

            cleanup_harbor() {
              rm -rf "$DOCKER_CONFIG"
              docker rmi "$BUILD_IMAGE" "$DEV_IMAGE" >/dev/null 2>&1 || true
            }
            trap cleanup_harbor EXIT HUP INT TERM

            mkdir -p "$DOCKER_CONFIG"

            echo "=== Harbor login with isolated Docker configuration ==="
            printf '%s' "$HARBOR_PASS" \
              | docker login "$HARBOR_REGISTRY" \
                  --username "$HARBOR_USER" \
                  --password-stdin

            echo ""
            echo "=== Building immutable and dev API tags ==="
            docker build \
              -t "$BUILD_IMAGE" \
              -t "$DEV_IMAGE" \
              api

            echo ""
            echo "=== Pushing immutable image ==="
            docker push "$BUILD_IMAGE"

            echo ""
            echo "=== Pushing dev alias ==="
            docker push "$DEV_IMAGE"

            echo ""
            echo "API image pushed:"
            echo "  $BUILD_IMAGE"
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

          IMAGE_TAG="${GIT_COMMIT:-dev}"
          FULL_IMAGE="${HARBOR_REGISTRY}/${HARBOR_PROJECT}/${API_IMAGE_NAME}:${IMAGE_TAG}"

          echo "Using kubeconfig file: $KUBECONFIG"
          test -r "$KUBECONFIG" || {
            echo "FAIL: Jenkins kubeconfig is missing or unreadable: $KUBECONFIG"
            exit 1
          }

          echo ""
          echo "=== Applying staging namespace ==="
          kubectl apply \
            -f kubernetes/drfarah-staging/namespace.yaml

          echo ""
          echo "=== Verifying required runtime Secrets ==="

          required_secrets="
            harbor-regcred
            drfarah-staging-db-secret
            drfarah-staging-api-secret
          "

          for secret in $required_secrets; do
            if kubectl -n "$STAGING_NAMESPACE" get secret "$secret" >/dev/null 2>&1; then
              echo "OK    Secret/$secret"
            else
              echo "FAIL  missing Secret/$secret"
              exit 1
            fi
          done

          echo ""
          echo "=== Applying PostgreSQL and API resources ==="

          kubectl apply \
            -f kubernetes/drfarah-staging/configmap.yaml \
            -f kubernetes/drfarah-staging/postgres-service.yaml \
            -f kubernetes/drfarah-staging/postgres-statefulset.yaml \
            -f kubernetes/drfarah-staging/api-service.yaml \
            -f kubernetes/drfarah-staging/api-ingress.yaml \
            -f kubernetes/drfarah-staging/api-deployment.yaml

          echo ""
          echo "=== Setting immutable API image ==="

          kubectl -n "$STAGING_NAMESPACE" \
            set image deployment/drfarah-staging-api \
            "api=$FULL_IMAGE"

          echo ""
          echo "=== Waiting for API rollout ==="

          kubectl -n "$STAGING_NAMESPACE" \
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
        sh '''
          set -eu

          echo "=== Staging API liveness ==="

          live_status="000"

          for attempt in $(seq 1 18); do
            live_status="$(
              curl -sS -o /dev/null -w '%{http_code}' \
                "${STAGING_API_URL}/api/v1/health/live" \
                || echo 000
            )"

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
              curl -sS -o /dev/null -w '%{http_code}' \
                "${STAGING_API_URL}/api/v1/health/ready" \
                || echo 000
            )"

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
          echo "=== Staging booking smoke test ==="

          RESPONSE_FILE="$(mktemp)"
          trap 'rm -f "$RESPONSE_FILE"' EXIT HUP INT TERM

          booking_status="$(
            curl -sS \
              -o "$RESPONSE_FILE" \
              -w '%{http_code}' \
              -X POST \
              -H 'Content-Type: application/json' \
              -d "{
                \"service_type\": \"CI smoke test\",
                \"visit_type\": \"Clinic visit\",
                \"preferred_day\": \"CI build ${BUILD_NUMBER}\",
                \"preferred_time\": \"9:00 AM\",
                \"time_window\": \"Morning\",
                \"first_name\": \"Jenkins\",
                \"last_name\": \"SmokeTest\",
                \"email\": \"smoke-test@example.com\",
                \"phone\": \"+1-555-000-0000\",
                \"reason_category\": \"General appointment request\"
              }" \
              "${STAGING_API_URL}/api/v1/bookings"
          )"

          if [ "$booking_status" != "201" ]; then
            echo "FAIL: booking smoke test returned HTTP $booking_status"
            echo "Safe response body:"
            cat "$RESPONSE_FILE"
            exit 1
          fi

          echo "Booking endpoint returned HTTP 201."

          grep -q '"id"' "$RESPONSE_FILE" || {
            echo "FAIL: booking response does not contain an id."
            cat "$RESPONSE_FILE"
            exit 1
          }

          echo "Booking response contains an id."
          echo ""
          echo "Staging API health and booking checks passed."
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
                echo 'Write access confirmed as:' \$(whoami)
              "

            echo ""
            echo "=== Deploying frontend to staging ==="

            rsync -av --delete \
              --exclude='.env' \
              --exclude='.well-known' \
              -e "ssh $SSH_OPTS" \
              frontend/ \
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$STAGING_DOCROOT/"

            echo ""
            echo "=== Staging frontend smoke test ==="

            frontend_status="000"

            for attempt in $(seq 1 10); do
              frontend_status="$(
                curl -sS -o /dev/null -w '%{http_code}' \
                  "https://${STAGING_FRONTEND_HOST}/" \
                  || echo 000
              )"

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

            curl -fsS "https://${STAGING_FRONTEND_HOST}/" \
              | grep -q 'Dr. Farah' || {
                echo "FAIL: Dr. Farah marker is absent."
                exit 1
              }

            curl -fsS "https://${STAGING_FRONTEND_HOST}/" \
              | grep -q 'noindex,nofollow,noarchive' || {
                echo "FAIL: noindex meta is absent."
                exit 1
              }

            curl -fsS "https://${STAGING_FRONTEND_HOST}/robots.txt" \
              | grep -q 'Disallow: /' || {
                echo "FAIL: robots.txt Disallow rule is absent."
                exit 1
              }

            deployed_paths="
              /styles.css
              /app.js
              /robots.txt
              /assets/logo-mark.svg
              /assets/favicon.svg
            "

            for path in $deployed_paths; do
              status="$(
                curl -sS -o /dev/null -w '%{http_code}' \
                  "https://${STAGING_FRONTEND_HOST}${path}"
              )"

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
  }

  post {
    success {
      echo 'SUCCESS — all stages required for this branch completed.'
    }

    failure {
      echo 'FAILURE — inspect the first failed stage and its diagnostics.'
    }

    always {
      sh '''
        rm -rf "$WORKSPACE"/.docker-auth-* >/dev/null 2>&1 || true
      '''
    }
  }
}
