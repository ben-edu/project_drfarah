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
  //
  // Does NOT:
  //   - Log in to Harbor or push images
  //   - Run kubectl or deploy to K3s
  //   - rsync to Hestia
  //   - Bind credentials of any kind
  //   - Deploy anything to any environment
  //
  // Deployment stages will be added in Step 03B.
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
            frontend/README.md
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
                pip install -q -r requirements.txt
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
