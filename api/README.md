# API — Dr. Farah VIP Urgent Care

FastAPI booking and administration API. Phase 1: booking MVP.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health/live` | Liveness probe (returns 200 when process is alive) |
| GET | `/api/v1/health/ready` | Readiness probe (returns 200 when database is reachable, 503 otherwise) |
| POST | `/api/v1/bookings` | **Legacy** — create a booking request (deprecated, preserved for backward compat) |
| GET | `/api/v1/services` | List active bookable services |
| GET | `/api/v1/availability` | Available appointment slots for a service and date range |
| POST | `/api/v1/appointments` | Create a scheduled appointment with conflict detection |
| POST | `/api/v1/patient-registrations` | Create a resumable patient-registration draft |
| GET | `/api/v1/patient-registrations/{reference}` | Resume a draft with the private registration token |
| PATCH | `/api/v1/patient-registrations/{reference}` | Save a patient-registration draft |
| POST | `/api/v1/patient-registrations/{reference}/submit` | Submit a completed registration |
| POST | `/api/v1/internal/cleanup-ci` | Clean up CI smoke-test records (token-protected) |

## Structure

```
api/
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── alembic.ini
├── alembic/
│   ├── env.py
│   └── versions/
│       ├── 0001_initial_bookings.py
│       ├── 0002_add_scheduling_tables.py
│       └── 0003_add_patient_registrations.py
├── app/
│   ├── main.py               App factory, router registration, lifespan
│   ├── core/
│   │   ├── config.py          Pydantic Settings (env-based, includes SMTP)
│   │   └── database.py        SQLAlchemy engine, session, Base
│   ├── models/
│   │   ├── booking.py         Legacy Booking model
│   │   ├── service.py         Service model
│   │   ├── working_hours.py   Working hours model
│   │   ├── blocked_period.py  Blocked period model
│   │   ├── appointment.py     Appointment model
│   │   └── patient_registration.py  Demographic/contact registration drafts
│   ├── routers/
│   │   ├── health.py          Health endpoints (/live, /ready)
│   │   ├── booking.py         Legacy booking endpoint
│   │   ├── appointments.py    Services, availability, appointments, cleanup
│   │   └── patient_registration.py  Save/resume/submit registration
│   ├── schemas/
│   │   ├── booking.py         Legacy booking schemas
│   │   ├── service.py         Service list schemas
│   │   ├── availability.py    Availability response schemas
│   │   ├── appointment.py     Appointment create/response schemas
│   │   └── patient_registration.py  Registration schemas
│   └── services/
│       ├── email.py           SMTP notification service
│       └── scheduling.py      Slot generation and conflict detection
└── tests/
    ├── conftest.py            Shared fixtures (isolated SQLite per test)
    ├── test_health.py         10 health/CORS tests
    ├── test_booking.py        12 legacy booking tests
    ├── test_services.py       7 service listing tests
    ├── test_availability.py   12 availability slot tests
    ├── test_appointments.py   16 appointment creation tests
    └── test_concurrency.py    3 concurrency/double-booking tests
```

## Running locally

```bash
cd api
pip install -r requirements.txt
PYTHONPATH=. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Running tests

```bash
cd api
pip install -r requirements.txt -r requirements-dev.txt
PYTHONPATH=. python -m pytest -q tests/
```

## Docker

The container runs as non-root `appuser`. The default SQLite path (`./drfarah.db`)
resolves to `/app/drfarah.db` which is not writable by `appuser`. For local
Docker runs, point `DATABASE_URL` to a writable location under `/tmp/`:

```bash
docker build -t drfarah-api:latest .
docker run -p 8000:8000 \
  -e ENVIRONMENT=test \
  -e DATABASE_URL='sqlite:////tmp/drfarah.db' \
  drfarah-api:latest
```

In staging/production, `DATABASE_URL` points to a real PostgreSQL instance
and `ENVIRONMENT` is `staging` or `prod`.

## Environment variables

| Variable | Default | Required |
|---|---|---|
| `APP_NAME` | `drfarah-api` | No |
| `ENVIRONMENT` | `dev` | No |
| `DATABASE_URL` | `sqlite:///./drfarah.db` | Yes (staging/prod) |
| `CORS_ORIGINS` | `https://staging.drfarahvipurgentcare.com` | No |
| `LOG_LEVEL` | `INFO` | No |
| `TRUST_PROXY` | `false` | Set to `true` behind Traefik/HAProxy |
| `SMTP_HOST` | `""` | Yes (for email notifications) |
| `SMTP_PORT` | `587` | No |
| `SMTP_USER` | `""` | Yes (for email notifications) |
| `SMTP_PASSWORD` | `""` | Yes (for email notifications) |
| `SMTP_FROM` | `""` | Yes (configured by environment) |
| `SMTP_TO` | `""` | Yes (configured by environment) |
| `SMTP_USE_TLS` | `true` | No |
| `SMTP_TEST_MODE` | `true` | No (set to `false` to send real emails) |
| `CLEANUP_TOKEN` | `""` | Yes (for CI cleanup endpoint) |

## Booking data discipline

The booking endpoint enforces strict validation:

- No clinical free text anywhere.
- Name fields accept only letters, hyphens, apostrophes, and spaces (validated via regex).
- Email must match standard pattern.
- Phone accepts only digits, +, -, (), and spaces.
- Reason category is selected from a predefined list (not free text).
- No insurance numbers, ID numbers, SSN, medical history, or documents.
- Request body is never logged.

## SMTP notification

- On each booking, `send_booking_notification()` is called.
- When `SMTP_TEST_MODE=true` (default for staging), the email content is logged instead of sent.
- When `SMTP_TEST_MODE=false` and SMTP is configured, emails are sent via SMTP+TLS.
- Failures in email sending are logged but do not block the booking response.
- SMTP credentials come from the Kubernetes Secret `drfarah-staging-api-secret`.

## Stack

- **Runtime:** Python 3.12
- **Framework:** FastAPI 0.115.6
- **Database:** SQLAlchemy 2.0 + psycopg (PostgreSQL)
- **Config:** pydantic-settings (environment-based)

## Staging deployment

- Harbor image: `harbor.proxbenovh.cloud/devops-project-harbor/drfarah-api:dev`
- K8s namespace: `drfarah-staging`
- API URL: `https://api-staging.drfarahvipurgentcare.com`
- Jenkins handles build, push, and manifest deployment on `dev` branch.

## Scheduling

See [`docs/architecture/SCHEDULING.md`](../docs/architecture/SCHEDULING.md)
for the full data model, slot generation algorithm, double-booking
protection, migration strategy, and CI cleanup mechanism.


## Online patient registration

The public registration flow is deliberately narrower than a full clinical intake:

- A new draft requires first name, last name, email, and phone.
- Patients receive a public registration reference plus a high-entropy private resume token.
- Only a SHA-256 hash of the resume token is stored in PostgreSQL.
- Drafts can be saved, resumed, and submitted electronically.
- Submitted registrations become read-only from the public endpoint.
- Clinic staff can review registrations through Keycloak-protected admin endpoints.
- This phase does **not** collect medical-history narratives, diagnoses, medication lists, insurance member IDs, SSNs, identity documents, or medical uploads.
- Request bodies are not intentionally logged by the application.

The narrower first phase is intentional so the clinic can approve the exact clinical forms and secure document workflow before more sensitive intake data is introduced.


## Final-domain environment split

Staging API: `https://api-staging.drfarahvipurgentcare.com`  
Production API: `https://api.drfarahvipurgentcare.com`

Staging and production use separate namespaces, PostgreSQL instances and
secrets. Brevo is the outbound transactional SMTP relay. Non-secret
host/from/to values are in each environment's ConfigMap; credentials remain in
the corresponding Kubernetes Secret. `SMTP_TO` accepts a comma-separated list,
and clinic recipients receive separate privacy-preserving notifications.
