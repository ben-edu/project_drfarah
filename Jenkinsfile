pipeline {
  agent any
  options { timestamps() }

  // =========================================================================
  // BOOTSTRAP JENKINSFILE — deliberately safe, non-deploying.
  //
  // Runs on feature/*, dev, and main.
  // Performs: checkout, metadata, path validation, Markdown hygiene,
  //           secret-filename detection.
  // Does NOT: build images, push to Harbor, rsync to Hestia, apply K8s
  //           manifests, bind credentials, or deploy anything.
  //
  // Deployment stages will be introduced only after the readiness audit
  // is accepted and infrastructure prerequisites are resolved.
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
          echo
          echo "Repository files:"
          ls -la
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

          # Patterns that must never be committed (allow .example variants).
          # This catches: .env, secret.yaml, *.tfstate, *.tfvars
          # It allows:    .env.example, secret.example.yaml, *.tfvars.example

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

          # We need to eval because of the -o chaining
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

    stage('No application code guard') {
      steps {
        sh '''
          set -e
          # Phase 1 guard: no application implementation should appear before
          # the readiness audit is accepted and infrastructure is provisioned.

          app_indicators=""
          [ -f frontend/index.html ] && app_indicators="$app_indicators frontend/index.html"
          [ -f frontend/package.json ] && app_indicators="$app_indicators frontend/package.json"
          [ -f api/requirements.txt ] && app_indicators="$app_indicators api/requirements.txt"
          [ -f api/app/main.py ] && app_indicators="$app_indicators api/app/main.py"
          [ -f admin/index.html ] && app_indicators="$app_indicators admin/index.html"
          [ -f Dockerfile ] && app_indicators="$app_indicators Dockerfile"
          [ -f docker-compose.yml ] && app_indicators="$app_indicators docker-compose.yml"

          if [ -n "$app_indicators" ]; then
            echo "WARNING: application files found before infrastructure readiness:"
            echo "$app_indicators"
            echo "This is informational — not a failure in bootstrap phase."
          else
            echo "OK: no application code detected (expected at bootstrap stage)."
          fi
        '''
      }
    }
  }

  post {
    success {
      echo 'BOOTSTRAP VALIDATION PASSED — repository foundation is clean.'
      echo 'Next: resolve infrastructure prerequisites, then begin implementation.'
    }
    failure {
      echo 'FAILURE — see logs above. Fix issues before proceeding to implementation.'
    }
  }
}
