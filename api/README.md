# API — Dr. Farah VIP Urgent Care

FastAPI booking and administration API. Phase 1: website + booking foundation.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/v1/health/live` | Liveness probe (returns 200 when process is alive) |
| GET | `/api/v1/health/ready` | Readiness probe (returns 200 when database is reachable, 503 otherwise) |

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

## Stack

- **Runtime:** Python 3.12
- **Framework:** FastAPI 0.115.6
- **Database:** SQLAlchemy 2.0 + psycopg (PostgreSQL)
- **Config:** pydantic-settings (environment-based)

## Status

Application scaffold and health checks implemented. Booking entities and
endpoints will be added in a later step. See `docs/READINESS_AUDIT.md` for
infrastructure readiness.
