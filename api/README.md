# API — Dr. Farah VIP Urgent Care

FastAPI booking and administration API. Phase 1: booking MVP.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health/live` | Liveness probe (returns 200 when process is alive) |
| GET | `/api/v1/health/ready` | Readiness probe (returns 200 when database is reachable, 503 otherwise) |
| POST | `/api/v1/bookings` | Create a booking request (returns 201 with booking data) |

## Structure

```
api/
├── Dockerfile
├── requirements.txt
├── requirements-dev.txt
├── README.md
├── app/
│   ├── main.py               App factory, router registration, table creation
│   ├── core/
│   │   ├── config.py          Pydantic Settings (env-based, includes SMTP)
│   │   └── database.py        SQLAlchemy engine, session, Base
│   ├── models/
│   │   └── booking.py         Booking SQLAlchemy model
│   ├── routers/
│   │   ├── health.py          Health endpoints (/live, /ready)
│   │   └── booking.py         Booking creation endpoint
│   ├── schemas/
│   │   └── booking.py         Pydantic request/response schemas
│   └── services/
│       └── email.py           SMTP notification service
└── tests/
    ├── test_health.py         10 health/CORS tests
    └── test_booking.py        12 booking tests
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

```bash
docker build -t drfarah-api:latest .
docker run -p 8000:8000 drfarah-api:latest
```

## Environment variables

| Variable | Default | Required |
|---|---|---|
| `APP_NAME` | `drfarah-api` | No |
| `ENVIRONMENT` | `dev` | No |
| `DATABASE_URL` | `sqlite:///./drfarah.db` | Yes (staging/prod) |
| `CORS_ORIGINS` | `https://staging.drfarah.proxbenovh.cloud` | No |
| `LOG_LEVEL` | `INFO` | No |
| `TRUST_PROXY` | `false` | Set to `true` behind Traefik/HAProxy |
| `SMTP_HOST` | `""` | Yes (for email notifications) |
| `SMTP_PORT` | `587` | No |
| `SMTP_USER` | `""` | Yes (for email notifications) |
| `SMTP_PASSWORD` | `""` | Yes (for email notifications) |
| `SMTP_FROM` | `noreply@drfarah.proxbenovh.cloud` | Yes |
| `SMTP_TO` | `appointments@drfarah.proxbenovh.cloud` | Yes |
| `SMTP_USE_TLS` | `true` | No |
| `SMTP_TEST_MODE` | `true` | No (set to `false` to send real emails) |

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
- API URL: `https://api.staging.drfarah.proxbenovh.cloud`
- Jenkins handles build, push, and manifest deployment on `dev` branch.
