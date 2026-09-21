"""Alembic migration environment.

Reads DATABASE_URL from the application Settings (environment variables).
Supports both PostgreSQL (staging/production) and SQLite (dev/test).

For SQLite, uses render_as_batch=True so ALTER TABLE works correctly.
"""

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# Ensure the api/ package is importable when running from the api/ directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Load application models so Base.metadata reflects all tables.
from app.core.database import Base  # noqa: E402
from app.models import booking  # noqa: E402,F401  — legacy bookings table

# Import scheduling models so they appear in Base.metadata.
import app.models.service  # noqa: E402,F401
import app.models.working_hours  # noqa: E402,F401
import app.models.blocked_period  # noqa: E402,F401
import app.models.appointment  # noqa: E402,F401

# Alembic Config object.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override sqlalchemy.url from the application Settings.
from app.core.config import get_settings  # noqa: E402

_settings = get_settings()
_database_url = _settings.effective_database_url
if _database_url:
    config.set_main_option("sqlalchemy.url", _database_url)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode — emit SQL without a live connection."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations against a live database."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        is_sqlite = connection.dialect.name == "sqlite"

        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=is_sqlite,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
