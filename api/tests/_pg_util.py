"""Shared helpers for PostgreSQL integration tests.

These tests require a real PostgreSQL server, provided by the CI stage
through POSTGRES_TEST_DATABASE_URL (a maintenance URL pointing at the
server's default database). No host orchestration (sudo/docker/subprocess)
happens here: disposable databases are created and dropped via ordinary
SQL on an AUTOCOMMIT connection. When the variable is absent, tests skip.
"""

import hashlib
import os
import re

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import make_url


def maintenance_url() -> str:
    """Return the server maintenance URL, or skip the test if not provided."""
    url = os.environ.get("POSTGRES_TEST_DATABASE_URL")
    if not url:
        pytest.skip(
            "POSTGRES_TEST_DATABASE_URL is not set; PostgreSQL integration "
            "tests require a running server (provided by the CI stage)."
        )
    return url


def normalize_pg(url_str: str):
    """Ensure the URL uses the psycopg (v3) driver, matching requirements.txt."""
    u = make_url(url_str)
    if u.drivername in ("postgresql", "postgres"):
        u = u.set(drivername="postgresql+psycopg")
    return u


def admin_engine():
    """AUTOCOMMIT engine bound to the server's maintenance database."""
    u = normalize_pg(maintenance_url())
    return create_engine(
        u, isolation_level="AUTOCOMMIT", connect_args={"connect_timeout": 5}
    )


def per_test_db_url(db_name: str) -> str:
    """Build the psycopg URL for a specific database on the same server."""
    u = normalize_pg(maintenance_url()).set(database=db_name)
    return u.render_as_string(hide_password=False)


def unique_db_name(prefix: str, node_name: str) -> str:
    """Derive a valid (<=63 char) PostgreSQL database name from a test name."""
    raw = re.sub(r"[^a-z0-9_]", "", node_name.replace(" ", "_").lower())
    name = f"{prefix}{raw}"
    if len(name) > 63:
        digest = hashlib.sha1(name.encode()).hexdigest()[:8]
        keep = 63 - len(prefix) - 9
        name = f"{prefix}{raw[:keep]}_{digest}"
    return name


def create_db(db_name: str) -> None:
    eng = admin_engine()
    try:
        with eng.connect() as conn:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
    finally:
        eng.dispose()


def terminate_and_drop(db_name: str) -> None:
    """Terminate lingering connections, then drop the database (idempotent)."""
    eng = admin_engine()
    try:
        with eng.connect() as conn:
            conn.execute(
                text(
                    "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
                    "WHERE datname = :n AND pid <> pg_backend_pid()"
                ),
                {"n": db_name},
            )
            conn.execute(text(f'DROP DATABASE IF EXISTS "{db_name}" WITH (FORCE)'))
    finally:
        eng.dispose()
