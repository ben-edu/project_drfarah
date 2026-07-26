# HANDOFF — 2026-07-26 (Step 07: Real Availability and Appointment Scheduling)

## Current state

- **Branch:** `feature/real-availability-scheduling`
- **Base:** `dev` (5ca8b47)
- **6 logical commits** (see SESSION_LOG.md for details)

## Work completed (Step 07 — Real Availability Scheduling)

### What changed

Replaced the free-text `preferred_day`/`preferred_time` booking system with
real appointment slots, availability generation, and double-booking prevention.

### New data models
- `Service` — bookable services with duration and buffer times
- `WorkingHours` — per-weekday operating hours with effective dates
- `BlockedPeriod` — clinic closure/unavailability periods
- `Appointment` — scheduled appointments with FK to services

### Alembic migrations
- `alembic` added to requirements, `alembic init` configured
- Migration 0001: captures existing `bookings` table (baseline)
- Migration 0002: creates scheduling tables + seeds provisional data
- PostgreSQL branch: `btree_gist` extension + exclusion constraint for
  double-booking prevention
- SQLite branch: plain index (no exclusion constraints in SQLite)

### New API endpoints
- `GET /api/v1/services` — list active services
- `GET /api/v1/availability` — available slots for date range
- `POST /api/v1/appointments` — create scheduled appointment with conflict
  detection
- `POST /api/v1/internal/cleanup-ci` — token-protected CI cleanup

### Legacy booking preserved
- `POST /api/v1/bookings` and `bookings` table unchanged
- Booking tests (12) and health tests (10) pass without modification
- Deprecation docstring added to booking router

### Frontend integration
- Services loaded dynamically from API
- Date picker (14-day rolling window) with clinic timezone
- Slot grid from availability endpoint with show-more toggle
- 409 conflict handling with "slot was just taken" message
- Loading/error states for all network operations
- Duplicate submission prevention

### Double-booking protection
- **Layer 1:** application-level conflict check (`check_slot_conflict`)
- **Layer 2:** PostgreSQL GiST exclusion constraint (`no_double_booking`)
- SQLite tests document the limitation; concurrent test skipped on SQLite

### CI updates
- Init container (`db-migrate`) in API Deployment runs migrations before
  main container starts
- Both containers set to immutable SHA at deploy time
- `CLEANUP_TOKEN` in ConfigMap for CI cleanup endpoint
- Jenkins health check: cleanup-ci, services, availability, appointment
  smoke test with `source="ci"`

### Tests
- 70 tests pass, 1 skipped (concurrency requires PostgreSQL)
- New test files: conftest.py, test_services.py, test_availability.py,
  test_appointments.py, test_concurrency.py
- Per-test isolated SQLite databases via tmp_path

### Provisional seed data
- 4 services (urgent-care, vip-mobile, traveler-care, rejuvenation)
- Working hours: Mon-Fri 9am-5pm Pacific
- Clearly marked as provisional — requires business confirmation

### Files changed (summarized)
| Area | Files |
|---|---|
| Models | 4 new (service, working_hours, blocked_period, appointment) |
| Schemas | 3 new (service, availability, appointment) |
| Routers | 1 new (appointments), 1 modified (booking deprecation) |
| Services | 1 new (scheduling) |
| Tests | 5 new (conftest + 4 test files) |
| Migrations | alembic.ini, env.py, 2 versions |
| Frontend | index.html, app.js updated |
| Kubernetes | api-deployment.yaml (init container), configmap.yaml (CLEANUP_TOKEN) |
| CI | Jenkinsfile (required paths, init container image, health check) |
| Docs | SCHEDULING.md, updated READMEs, HANDOFF.md, SESSION_LOG.md |

### What was NOT done
- No SMTP, secret, or password changes
- No RBAC changes
- No production deployment
- No frontend visual redesign
- No admin UI, Keycloak, HAProxy, DNS, or TLS changes
- No PR merge (awaiting operator review)

## Recommended next step

1. Push the branch and open a PR into `dev`.
2. After merge, trigger a `dev` build in Jenkins.
3. Verify the init container runs migrations successfully.
4. Verify the new endpoints respond correctly.
5. Confirm the CI cleanup + appointment smoke test pass.

Do not start Keycloak/admin UI until scheduling is verified end-to-end.
