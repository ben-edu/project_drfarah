pipeline {
  agent any
  options { timestamps() }

  // =========================================================================
  // JENKINSFILE — Phase 1 (test, build, staging deploy).
  //
  // Runs on feature/*, dev, and main.
  //
  // Does:
  //   - Checkout, metadata, path validation
  //   - Secret-filename detection
  //   - Markdown hygiene
  //   - API tests (in container)
  //   - Frontend file/JS/serving/no-index validation
  //   - API Docker build and push to Harbor (dev only)
  //   - API staging manifest deploy and rollout (dev only)
  //   - API staging health check + booking smoke test (dev only)
  //   - Frontend staging deployment (dev only, rsync to Hestia via benweb SSH)
  //
  // Does NOT:
  //   - Deploy to production (main)
  //   - Deploy API, admin, or database to production
  //   - Modify HAProxy, DNS, TLS, or Hestia config
  //
  // Feature branches: validation only.
  // Dev: validation + API build/push + API deploy + frontend staging deploy.
  // Main: validation only (production deploy not yet configured).
  // =========================================================================

  stages {

    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build metadata') {
      steps {
        sh '''
          set -e
          echo "========================================="
          echo "Project:     drfarah"
          echo "Branch:      ${GIT_BRANCH:-unknown}"
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
          set -e

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
            api/app/models/booking.py
            api/app/schemas/booking.py
            api/app/routers/booking.py
            api/app/services/email.py
            api/tests/test_booking.py
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
          echo "All required paths present."
        '''
      }
    }

    stage('Detect committed secret filenames') {
      steps {
        sh '''
          set -e

          forbidden_patterns="
            -name .env
            -o -name secret.yaml
            -o -name secrets.yaml
            -o -name '*.tfstate'
            -o -name '*.tfvars'
            -o -name credentials.json
            -o -name service-account-key.json
            -o -name 'id_rsa'
            -o -name 'id_ed25519'
            -o -name '*.pem'
          "

          hits=$(eval find . \\( $forbidden_patterns \\) -not -name '*.example' -not -path './.git/*' 2>/dev/null) || true

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
          set -e
          echo "Checking Markdown files for basic readability..."
          md_files=$(find . -name "*.md" -not -path "./.git/*" | sort)
          if [ -z "$md_files" ]; then
            echo "No Markdown files found — nothing to check."
          else
            for f in $md_files; do
              lines=$(wc -l < "$f")
              echo "  $f  ($lines lines)"
            done
            echo "Markdown file count: $(echo "$md_files" | wc -l)"
          fi
        '''
      }
    }

    stage('API — tests') {
      when {
        anyOf {
          branch 'dev'
          branch 'main'
          branch pattern: 'feature/.*', comparator: 'REGEXP'
        }
      }
      steps {
        dir('api') {
          sh '''
            set -e
            # Agent has no python3-venv — run tests inside a container.
            # Read-only mount + PYTHONDONTWRITEBYTECODE prevents root-owned
            # __pycache__ from contaminating the Jenkins workspace.
            echo "Running API tests in python:3.12-slim container (read-only workspace)..."
            docker run --rm \
              -v "$PWD":/app:ro \
              -w /app \
              -e PYTHONDONTWRITEBYTECODE=1 \
              -e PYTHONPYCACHEPREFIX=/tmp/pycache \
              python:3.12-slim \
              bash -c "
                set -e
                pip install -q -r requirements.txt -r requirements-dev.txt
                PYTHONPATH=. python -m pytest -q -p no:cacheprovider tests/
              "
          '''
        }
      }
    }

    stage('API — Docker build validation') {
      when {
        anyOf {
          branch 'dev'
          branch 'main'
          branch pattern: 'feature/.*', comparator: 'REGEXP'
        }
      }
      steps {
        dir('api') {
          sh '''
            set -euo pipefail

            CONTAINER_NAME="drfarah-api-validation-${BUILD_NUMBER}"
            IMAGE_NAME="drfarah-api:test-build"
            HOST_PORT="$((18000 + BUILD_NUMBER % 100))"

            cleanup() {
              docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
            }
            trap cleanup EXIT

            echo "=== Building Docker image ==="
            docker build -t "$IMAGE_NAME" .
            echo "Docker build successful."

            echo "=== Starting validation container (port=$HOST_PORT) ==="
            docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true

            docker run -d \\
              --name "$CONTAINER_NAME" \\
              -p "${HOST_PORT}:8000" \\
              -e ENVIRONMENT=test \\
              -e DATABASE_URL='sqlite:////tmp/drfarah-validation.db' \\
              "$IMAGE_NAME"

            echo "=== Waiting for liveness endpoint ==="
            healthy=0
            for attempt in $(seq 1 20); do
              state="$(docker inspect -f '{{.State.Status}}' "$CONTAINER_NAME" 2>/dev/null || echo missing)"
              if [ "$state" = "exited" ] || [ "$state" = "dead" ]; then
                echo "  Container exited unexpectedly (state=$state) — aborting."
                break
              fi

              if curl -fsS "http://127.0.0.1:${HOST_PORT}/api/v1/health/live" >/dev/null 2>&1; then
                healthy=1
                break
              fi

              echo "  attempt $attempt/20 — not ready yet..."
              sleep 1
            done

            if [ "$healthy" -ne 1 ]; then
              echo ""
              echo "=== FAILURE: container did not become healthy ==="
              echo ""
              echo "--- docker ps ---"
              docker ps -a --filter "name=$CONTAINER_NAME" || true
              echo ""
              echo "--- container state ---"
              docker inspect "$CONTAINER_NAME" \\
                --format 'status={{.State.Status}} exit={{.State.ExitCode}} error={{.State.Error}}' \\
                || true
              echo ""
              echo "--- container logs (last 200 lines) ---"
              docker logs --tail 200 "$CONTAINER_NAME" || true
              exit 1
            fi

            echo ""
            echo "=== Liveness check passed ==="
            HEALTH=$(curl -fsS "http://127.0.0.1:${HOST_PORT}/api/v1/health/live")
            echo "Health response: $HEALTH"

            echo ""
            echo "=== Readiness check ==="
            READY=$(curl -fsS "http://127.0.0.1:${HOST_PORT}/api/v1/health/ready")
            echo "Ready response: $READY"

            echo ""
            echo "=== Container validation passed ==="

            # Clean up the test image to avoid disc clutter on the agent.
            docker rmi "$IMAGE_NAME" >/dev/null 2>&1 || true
          '''
        }
      }
    }

    stage('Frontend — validation') {
      when {
        anyOf {
          branch 'dev'
          branch 'main'
          branch pattern: 'feature/.*', comparator: 'REGEXP'
        }
      }
      steps {
        sh '''
          set -e

          echo "=== Frontend: checking required files ==="
          required="
            frontend/index.html
            frontend/styles.css
            frontend/app.js
            frontend/robots.txt
          "
          for f in $required; do
            if [ -f "$f" ]; then
              echo "OK    $f"
            else
              echo "MISS  $f"
              exit 1
            fi
          done

          echo ""
          echo "=== Frontend: JavaScript syntax check ==="
          docker run --rm \
            -v "$PWD":/app \
            -w /app \
            node:20-slim \
            node --check frontend/app.js
          echo "JS syntax OK."

          echo ""
          echo "=== Frontend: no-index protection check ==="
          grep -q 'noindex,nofollow,noarchive' frontend/index.html || {
            echo "FAIL: missing noindex meta tag in frontend/index.html"
            exit 1
          }
          echo "OK: noindex meta tag present."

          grep -q 'Disallow: /' frontend/robots.txt || {
            echo "FAIL: missing Disallow rule in frontend/robots.txt"
            exit 1
          }
          echo "OK: robots.txt Disallow rule present."

          echo ""
          echo "=== Frontend: static asset serving check ==="
          SERVER_PID=""
          cleanup_server() {
            if [ -n "$SERVER_PID" ] && kill -0 "$SERVER_PID" 2>/dev/null; then
              kill "$SERVER_PID" 2>/dev/null || true
              wait "$SERVER_PID" 2>/dev/null || true
              echo "Static server stopped."
            fi
          }
          trap cleanup_server EXIT

          PORT=18900
          cd frontend
          python3 -m http.server "$PORT" --bind 127.0.0.1 &
          SERVER_PID=$!
          cd ..
          sleep 1

          if ! kill -0 "$SERVER_PID" 2>/dev/null; then
            echo "FAIL: static server did not start"
            exit 1
          fi
          echo "Static server started on port $PORT (PID $SERVER_PID)."

          for path in / /styles.css /app.js /robots.txt; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT$path")
            if [ "$STATUS" = "200" ]; then
              echo "OK    $path -> $STATUS"
            else
              echo "FAIL  $path -> $STATUS"
              exit 1
            fi
          done

          echo ""
          echo "=== Frontend: asset serving check ==="
          asset_paths="
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
          for path in $asset_paths; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:$PORT$path")
            if [ "$STATUS" = "200" ]; then
              echo "OK    $path -> $STATUS"
            else
              echo "FAIL  $path -> $STATUS"
              exit 1
            fi
          done

          echo ""
          echo "=== Frontend validation passed ==="
        '''
      }
    }

    stage('API — build and push to Harbor') {
      when {
        branch 'dev'
      }
      steps {
        withCredentials([usernamePassword(
            credentialsId: 'harbor-robot-devops-project-harbor',
            usernameVariable: 'HARBOR_USER',
            passwordVariable: 'HARBOR_PASS'
        )]) {
          sh '''
            set -e

            HARBOR_REGISTRY=harbor.proxbenovh.cloud
            HARBOR_REPO=devops-project-harbor/drfarah-api
            IMAGE_TAG="${GIT_COMMIT:-dev}"

            echo "=== Building API Docker image ==="
            cd api
            docker build -t "$HARBOR_REGISTRY/$HARBOR_REPO:$IMAGE_TAG" -t "$HARBOR_REGISTRY/$HARBOR_REPO:dev" .

            echo "=== Logging in to Harbor ==="
            echo "$HARBOR_PASS" | docker login "$HARBOR_REGISTRY" -u "$HARBOR_USER" --password-stdin

            echo "=== Pushing to Harbor ==="
            docker push "$HARBOR_REGISTRY/$HARBOR_REPO:$IMAGE_TAG"
            docker push "$HARBOR_REGISTRY/$HARBOR_REPO:dev"

            echo "=== Logging out ==="
            docker logout "$HARBOR_REGISTRY"

            echo "=== Image pushed: $HARBOR_REGISTRY/$HARBOR_REPO:$IMAGE_TAG ==="
          '''
        }
      }
    }

    stage('API — deploy staging manifests') {
      when {
        branch 'dev'
      }
      steps {
        withKubeConfig([credentialsId: 'kubeconfig-proxbenovh']) {
          sh '''
            set -e

            echo "=== Ensuring drfarah-staging namespace ==="
            kubectl apply -f kubernetes/drfarah-staging/namespace.yaml

            echo "=== Applying API manifests ==="
            kubectl apply -f kubernetes/drfarah-staging/api-service.yaml
            kubectl apply -f kubernetes/drfarah-staging/api-ingress.yaml

            echo "=== Patching API deployment image tag ==="
            IMAGE_TAG="${GIT_COMMIT:-dev}"
            kubectl set image deployment/drfarah-staging-api \
              -n drfarah-staging \
              "api=harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api:$IMAGE_TAG"

            echo "=== Applying API deployment ==="
            kubectl apply -f kubernetes/drfarah-staging/api-deployment.yaml

            echo "=== Waiting for rollout ==="
            kubectl rollout status deployment/drfarah-staging-api -n drfarah-staging --timeout=120s
          '''
        }
      }
    }

    stage('API — staging health check') {
      when {
        branch 'dev'
      }
      steps {
        sh '''
          set -e

          STAGING_API=https://api.staging.drfarah.proxbenovh.cloud

          echo "=== Checking staging API liveness ==="
          for i in 1 2 3 4 5; do
            STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_API/api/v1/health/live")
            if [ "$STATUS" = "200" ]; then
              echo "Liveness OK (attempt $i)"
              break
            fi
            echo "Waiting... (attempt $i, status $STATUS)"
            sleep 5
          done

          if [ "$STATUS" != "200" ]; then
            echo "FAIL: staging API liveness probe failed"
            exit 1
          fi

          echo ""
          echo "=== Checking staging API readiness ==="
          READY_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$STAGING_API/api/v1/health/ready")
          if [ "$READY_STATUS" = "200" ]; then
            echo "Readiness OK ($READY_STATUS)"
          else
            echo "FAIL: readiness returned $READY_STATUS"
            exit 1
          fi

          echo ""
          echo "=== Smoke-test booking endpoint ==="
          BOOKING_STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
            -H "Content-Type: application/json" \
            -d '{"service_type":"Test check","visit_type":"Clinic visit","preferred_day":"Monday","preferred_time":"9:00 AM","first_name":"Smoke","last_name":"Test","email":"test@example.com","phone":"+1-555-0000","reason_category":"General"}' \
            "$STAGING_API/api/v1/bookings")
          if [ "$BOOKING_STATUS" = "201" ]; then
            echo "Booking endpoint OK ($BOOKING_STATUS)"
          else
            echo "WARNING: booking endpoint returned $BOOKING_STATUS (may need DB)"
          fi

          echo ""
          echo "=== Staging API health check passed ==="
        '''
      }
    }

    stage('Frontend — deploy staging') {
      when {
        branch 'dev'
      }
      steps {
        withCredentials([sshUserPrivateKey(
            credentialsId: 'hestia-benweb-ssh',
            keyFileVariable: 'SSH_KEY'
        )]) {
          sh '''
            set -e

            HESTIA_SSH_HOST=192.168.100.75
            HESTIA_SSH_PORT=2275
            HESTIA_SSH_USER=benweb
            STAGING_FRONTEND_HOST=staging.drfarah.proxbenovh.cloud
            STAGING_DOCROOT=/home/benweb/web/staging.drfarah.proxbenovh.cloud/public_html

            SSH_OPTS="-i $SSH_KEY -p $HESTIA_SSH_PORT -o StrictHostKeyChecking=accept-new -o BatchMode=yes"

            echo "=== Preflight: verify docroot and write access ==="
            ssh $SSH_OPTS "$HESTIA_SSH_USER@$HESTIA_SSH_HOST" "
              set -e
              [ -d '$STAGING_DOCROOT' ] || { echo 'ERROR: docroot missing'; exit 1; }
              touch '$STAGING_DOCROOT/.wtest' 2>/dev/null || { echo 'ERROR: no write access as '\\$(whoami); ls -ld '$STAGING_DOCROOT'; exit 1; }
              rm -f '$STAGING_DOCROOT/.wtest'
              echo 'Preflight OK — docroot exists, write confirmed ('\\$(whoami)')'
            "

            echo ""
            echo "=== Deploying frontend to staging ==="
            rsync -av --delete \\
              --exclude='.env' \\
              --exclude='.well-known' \\
              -e "ssh $SSH_OPTS" \\
              frontend/ \\
              "$HESTIA_SSH_USER@$HESTIA_SSH_HOST:$STAGING_DOCROOT/"

            echo ""
            echo "=== Smoke test ==="
            SMOKE_STATUS=""
            for i in 1 2 3 4 5; do
              SMOKE_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$STAGING_FRONTEND_HOST/")
              if [ "$SMOKE_STATUS" = "200" ]; then
                echo "Smoke test OK (attempt $i)"
                break
              fi
              echo "Waiting... (attempt $i, status $SMOKE_STATUS)"
              sleep 3
            done

            if [ "$SMOKE_STATUS" != "200" ]; then
              echo "FAIL: staging frontend not reachable after deploy"
              exit 1
            fi

            echo ""
            echo "=== Content verification ==="
            curl -sS "https://$STAGING_FRONTEND_HOST/" | grep -q 'Dr. Farah' || {
              echo "FAIL: Dr. Farah marker not found in deployed page"
              exit 1
            }
            echo "OK: Dr. Farah marker present."

            curl -sS "https://$STAGING_FRONTEND_HOST/" | grep -q 'noindex,nofollow,noarchive' || {
              echo "FAIL: noindex meta missing in deployed page"
              exit 1
            }
            echo "OK: noindex meta present."

            curl -sS "https://$STAGING_FRONTEND_HOST/robots.txt" | grep -q 'Disallow: /' || {
              echo "FAIL: Disallow rule missing in deployed robots.txt"
              exit 1
            }
            echo "OK: robots.txt Disallow rule present."

            echo ""
            echo "=== Asset verification ==="
            for path in /styles.css /app.js /robots.txt; do
              ASSET_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://$STAGING_FRONTEND_HOST$path")
              if [ "$ASSET_STATUS" = "200" ]; then
                echo "OK    $path -> $ASSET_STATUS"
              else
                echo "FAIL  $path -> $ASSET_STATUS"
                exit 1
              fi
            done

            echo ""
            echo "=== Staging deployment complete ==="
          '''
        }
      }
    }
  }

  post {
    success {
      echo 'BUILD PASSED — all checks, tests, and Docker build validation succeeded.'
    }
    failure {
      echo 'FAILURE — see logs above. Fix issues before proceeding.'
    }
  }
}
