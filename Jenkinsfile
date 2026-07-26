pipeline {
  agent any
  options { timestamps() }

  // =========================================================================
  // JENKINSFILE — Phase 1 (test and build validation only).
  //
  // Runs on feature/*, dev, and main.
  //
  // Does:
  //   - Checkout, metadata, path validation
  //   - Secret-filename detection
  //   - Markdown hygiene
  //   - API tests (in container)
  //   - Docker image build validation
  //   - Frontend file/JS/serving/no-index validation
  //   - Frontend staging deployment (dev only, rsync to Hestia via benweb SSH)
  //
  // Does NOT:
  //   - Log in to Harbor or push images
  //   - Run kubectl or deploy to K3s
  //   - Deploy to production frontend (main)
  //   - Deploy API, admin, or database
  //   - Modify HAProxy, DNS, TLS, or Hestia config
  //
  // Feature branches: validation only.
  // Dev: validation + staging deployment.
  // Main: validation only (production frontend deploy not yet configured).
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
            frontend/README.md
            frontend/index.html
            frontend/styles.css
            frontend/app.js
            frontend/robots.txt
            admin/README.md
            api/README.md
            kubernetes/drfarah/README.md
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
            echo "Running API tests in python:3.12-slim container..."
            docker run --rm \
              -v "$PWD":/app \
              -w /app \
              python:3.12-slim \
              bash -c "
                set -e
                pip install -q -r requirements.txt -r requirements-dev.txt
                PYTHONPATH=. python -m pytest -q tests/
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
            set -e
            echo "Validating Docker image build..."
            docker build -t drfarah-api:test-build .
            echo "Docker build successful."

            echo "Running container health check..."
            CONTAINER_ID=$(docker run -d -p 18000:8000 drfarah-api:test-build)
            sleep 5
            HEALTH=$(curl -fsS http://localhost:18000/api/v1/health/live 2>&1)
            echo "Health response: $HEALTH"
            docker stop "$CONTAINER_ID"
            docker rm "$CONTAINER_ID"

            # Clean up the test image to avoid disc clutter on the agent.
            docker rmi drfarah-api:test-build || true
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
          echo "=== Frontend validation passed ==="
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
