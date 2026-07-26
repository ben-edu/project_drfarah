# Real Availability and Appointment Scheduling

## Overview

Replaces the legacy free-text `preferred_day`/`preferred_time` booking model
with real appointment slots, availability generation, and double-booking
prevention backed by PostgreSQL exclusion constraints.

The legacy `POST /api/v1/bookings` endpoint and `bookings` table are preserved
for backward compatibility. New integrations should use the scheduling
endpoints.

## Data model

### services

| Column | Type | Description |
|---|---|---|
| id | int (PK) | Auto-increment |
| code | varchar(64) UNIQUE | Machine-readable identifier (e.g. `urgent-care`) |
| name | varchar(128) | Human-readable name |
| description | text | Optional description |
| duration_minutes | int | Appointment duration (not including buffers) |
| buffer_before_minutes | int | Buffer time before appointment (default 0) |
| buffer_after_minutes | int | Buffer time after appointment (default 0) |
| is_active | bool | Whether the service is bookable |
| created_at | timestamp | Auto-set |
| updated_at | timestamp | Auto-set |

**Provisional seed data (4 services):**

| code | name | Duration | Buffer before | Buffer after |
|---|---|---|---|---|
| urgent-care | Urgent or acute care | 30 min | 0 | 0 |
| vip-mobile | VIP or mobile visit | 45 min | 15 min | 15 min |
| traveler-care | Traveler medical care | 30 min | 0 | 0 |
| rejuvenation | Rejuvenation consultation | 60 min | 15 min | 15 min |

These are provisional — they require business confirmation before production.
To change: update the migration seed data, or use the admin UI (future).

### working_hours

| Column | Type | Description |
|---|---|---|
| id | int (PK) | Auto-increment |
| weekday | int | 0=Monday through 6=Sunday |
| start_time | time | Opening time (clinic timezone) |
| end_time | time | Closing time (clinic timezone) |
| is_active | bool | Whether this rule is active |
| effective_from | date | Start of validity period |
| effective_until | date (nullable) | End of validity period (null = open-ended) |

**Provisional seed data:** Monday-Friday 9:00 AM – 5:00 PM Pacific.
Requires business confirmation before production.

### blocked_periods

| Column | Type | Description |
|---|---|---|
| id | int (PK) | Auto-increment |
| starts_at | timestamptz | Block start (UTC) |
| ends_at | timestamptz | Block end (UTC) |
| reason | varchar(256) (nullable) | Reason for block |
| is_active | bool | Whether this block is enforced |
| created_at | timestamptz | Auto-set |
| updated_at | timestamptz | Auto-set |

Represents any period when appointments cannot be scheduled: holidays,
breaks, physician unavailability, manual blocks.

### appointments

| Column | Type | Description |
|---|---|---|
| id | int (PK) | Auto-increment |
| service_id | int (FK → services) | Selected service |
| starts_at | timestamptz | Appointment start (UTC) |
| ends_at | timestamptz | Appointment end (UTC) |
| timezone | varchar(64) | Clinic timezone |
| first_name | varchar(128) | Patient first name |
| last_name | varchar(128) | Patient last name |
| email | varchar(255) | Contact email |
| phone | varchar(64) | Contact phone |
| reason_category | varchar(128) | Predefined reason |
| status | varchar(32) | pending/confirmed/cancelled/completed/no_show |
| source | varchar(64) (nullable) | Internal marker (e.g. `ci`) |
| created_at | timestamptz | Auto-set |
| updated_at | timestamptz | Auto-set |

## Timezone handling

- **Clinic timezone:** `America/Los_Angeles` (Pacific)
- **Storage:** all timestamps stored in UTC (`timestamptz`)
- **API input:** ISO 8601 with timezone offset required (e.g. `2026-07-28T09:00:00-07:00`)
- **API output:** ISO 8601 with UTC offset

## Slot generation algorithm

`app/services/scheduling.py — generate_availability()`

1. Load working-hour intervals active for the requested date range.
2. Group working hours by weekday.
3. Load blocked periods and existing non-cancelled appointments overlapping the range.
4. For each day in the range:
   a. Find working-hour intervals for the day's weekday.
   b. Starting from opening time + buffer_before, generate slots at 15-minute increments.
   c. Each slot's occupied range = [start - buffer_before, start + duration + buffer_after).
   d. Skip slots where the occupied range falls outside working hours.
   e. Skip slots where the occupied range overlaps a blocked period.
   f. Skip slots where the occupied range overlaps an existing non-cancelled appointment.
   g. Skip slots that start in the past.
5. Return slots as `[{starts_at, ends_at}]` dicts.

**Constants:**
- Slot increment: 15 minutes
- Maximum availability range: 31 days

## Double-booking prevention

### Layer 1 — Application-level conflict check

`app/services/scheduling.py — check_slot_conflict()`

Before inserting an appointment, queries for any existing non-cancelled
appointment whose range overlaps the occupied range (slot + buffers) of
the new appointment.

### Layer 2 — PostgreSQL exclusion constraint

Migration 0002 creates a GiST exclusion constraint (PostgreSQL only):

```sql
CREATE EXTENSION IF NOT EXISTS btree_gist;

ALTER TABLE appointments ADD CONSTRAINT no_double_booking
  EXCLUDE USING GIST (
    tstzrange(starts_at, ends_at, '[)') WITH &&
  ) WHERE (status NOT IN ('cancelled', 'no_show'));
```

- `[)` range: includes start, excludes end
- WHERE clause: cancelled/no_show appointments don't block slots
- Requires `btree_gist` extension (bundled with PostgreSQL 16, no external install)

This prevents the SELECT-then-INSERT race condition that application-level
checks cannot prevent under concurrent requests.

### SQLite test limitation

SQLite has no GiST indexes, exclusion constraints, or `btree_gist`. Tests
use application-level conflict detection only. Concurrent-write tests
document this limitation and are skipped when running against SQLite.

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/services` | List active services |
| GET | `/api/v1/availability` | Available slots for a date range |
| POST | `/api/v1/appointments` | Create a scheduled appointment |
| POST | `/api/v1/internal/cleanup-ci` | Clean up CI smoke-test records (token-protected) |
| POST | `/api/v1/bookings` | **Legacy** — preserved for backward compatibility |

## CI cleanup mechanism

The internal endpoint `POST /api/v1/internal/cleanup-ci` requires a
pre-shared token (`Authorization: Bearer <token>`) and deletes
appointments where `source='ci'` and `created_at < now() - 1 hour`.

- Token stored in ConfigMap (operational, not a secret)
- Only deletes CI-marked records — never touches real appointments
- 1-hour grace period prevents race conditions
- Jenkins calls this before each smoke test to clean up previous runs

## Migrations

Two Alembic migrations manage the schema:

1. **0001_initial_bookings** — captures the existing `bookings` table schema.
   In staging, this is stamped as already-applied (the table exists from
   the earlier `create_all()` era).

2. **0002_add_scheduling_tables** — creates services, working_hours,
   blocked_periods, and appointments tables. Seeds provisional data.
   PostgreSQL branch: adds `btree_gist` extension and exclusion constraint.
   SQLite branch: adds a plain index for query performance.

Migration execution: an init container (`db-migrate`) in the API Deployment
runs `python -m alembic upgrade head` before the main API container starts.
If the migration fails, the init container exits non-zero, the pod stays in
Init phase, and the old pod keeps running (Kubernetes does not terminate
the old pod until the new pod is Ready).

## Out of scope

- Admin UI for managing services, working hours, blocked periods
- Keycloak authentication
- Email notifications for scheduled appointments
- Production deployment
- Patient portal or self-service cancellation
