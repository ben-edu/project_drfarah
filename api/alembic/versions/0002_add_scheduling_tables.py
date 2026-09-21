"""Add scheduling tables — services, working_hours, blocked_periods, appointments.

Revision ID: 0002
Revises: 0001
Create Date: 2026-07-26

Includes provisional seed data for services and working hours. Seed data
must be reviewed and confirmed by the clinic before production use.

Adds a PostgreSQL exclusion constraint for double-booking prevention.
SQLite databases receive a plain index instead (no exclusion constraint).
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "0002"
down_revision: Union[str, None] = "0001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# ---------------------------------------------------------------------------
# PROVISIONAL SEED DATA — requires business confirmation before production.
# These values are placeholders for development and staging only.
# To change: update the seed data or use the admin UI (future).
# ---------------------------------------------------------------------------

SERVICES = [
    {"code": "urgent-care", "name": "Urgent or acute care",
     "description": "Same-day illness, injury, or immediate concern.",
     "duration_minutes": 30, "buffer_before_minutes": 0, "buffer_after_minutes": 0},
    {"code": "vip-mobile", "name": "VIP or mobile visit",
     "description": "Discreet physician visits for hotels, offices, and residences.",
     "duration_minutes": 45, "buffer_before_minutes": 15, "buffer_after_minutes": 15},
    {"code": "traveler-care", "name": "Traveler medical care",
     "description": "Care for tourists, executives, and business travelers.",
     "duration_minutes": 30, "buffer_before_minutes": 0, "buffer_after_minutes": 0},
    {"code": "rejuvenation", "name": "Rejuvenation consultation",
     "description": "PRP, PRF, skin, hair, and recovery consultations.",
     "duration_minutes": 60, "buffer_before_minutes": 15, "buffer_after_minutes": 15},
]

# PROVISIONAL — placeholder hours. Monday-Friday, 9 AM – 5 PM Pacific.
# Real clinic hours TBD by Dr. Farah's practice.
WORKING_HOURS = [
    {"weekday": d, "start": "09:00", "end": "17:00"}
    for d in range(0, 5)  # 0=Monday .. 4=Friday
]


def _is_postgresql() -> bool:
    """Return True if the current connection is PostgreSQL."""
    conn = op.get_bind()
    return conn.dialect.name == "postgresql"


def upgrade() -> None:
    is_pg = _is_postgresql()

    # ------------------------------------------------------------------
    # btree_gist extension (PostgreSQL only) — required for the partial
    # exclusion constraint on the appointments table.
    # ------------------------------------------------------------------
    if is_pg:
        op.execute("CREATE EXTENSION IF NOT EXISTS btree_gist")

    # ------------------------------------------------------------------
    # services
    # ------------------------------------------------------------------
    op.create_table(
        "services",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("name", sa.String(length=256), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("duration_minutes", sa.Integer(), nullable=False),
        sa.Column("buffer_before_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("buffer_after_minutes", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("code"),
    )
    op.create_index(op.f("ix_services_code"), "services", ["code"], unique=True)

    # Seed services.
    services_table = sa.table(
        "services",
        sa.column("code", sa.String),
        sa.column("name", sa.String),
        sa.column("description", sa.Text),
        sa.column("duration_minutes", sa.Integer),
        sa.column("buffer_before_minutes", sa.Integer),
        sa.column("buffer_after_minutes", sa.Integer),
    )
    op.bulk_insert(services_table, SERVICES)

    # ------------------------------------------------------------------
    # working_hours
    # ------------------------------------------------------------------
    op.create_table(
        "working_hours",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("weekday", sa.Integer(), nullable=False),
        sa.Column("start_time", sa.Time(), nullable=False),
        sa.Column("end_time", sa.Time(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("effective_from", sa.Date(), nullable=False),
        sa.Column("effective_until", sa.Date(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_working_hours_weekday"), "working_hours", ["weekday"], unique=False)

    # Seed working hours.
    from datetime import date, time
    working_hours_table = sa.table(
        "working_hours",
        sa.column("weekday", sa.Integer),
        sa.column("start_time", sa.Time),
        sa.column("end_time", sa.Time),
        sa.column("effective_from", sa.Date),
    )
    op.bulk_insert(
        working_hours_table,
        [
            {
                "weekday": wh["weekday"],
                "start_time": time.fromisoformat(wh["start"]),
                "end_time": time.fromisoformat(wh["end"]),
                "effective_from": date(2026, 1, 1),
            }
            for wh in WORKING_HOURS
        ],
    )

    # ------------------------------------------------------------------
    # blocked_periods
    # ------------------------------------------------------------------
    op.create_table(
        "blocked_periods",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reason", sa.String(length=256), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    # ------------------------------------------------------------------
    # appointments
    # ------------------------------------------------------------------
    op.create_table(
        "appointments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("service_id", sa.Integer(), nullable=False),
        sa.Column("starts_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ends_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("timezone", sa.String(length=64), nullable=False, server_default="America/Los_Angeles"),
        sa.Column("first_name", sa.String(length=128), nullable=False),
        sa.Column("last_name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=64), nullable=False),
        sa.Column("reason_category", sa.String(length=128), nullable=False),
        sa.Column(
            "status", sa.String(length=32), nullable=False, server_default="pending",
        ),
        sa.Column("source", sa.String(length=32), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True),
            server_default=sa.func.now(), nullable=False,
        ),
        sa.ForeignKeyConstraint(["service_id"], ["services.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_appointments_starts_at"), "appointments", ["starts_at"], unique=False)
    op.create_index(op.f("ix_appointments_status"), "appointments", ["status"], unique=False)

    # ------------------------------------------------------------------
    # Double-booking protection
    # ------------------------------------------------------------------
    if is_pg:
        op.execute(
            "ALTER TABLE appointments ADD CONSTRAINT no_double_booking "
            "EXCLUDE USING GIST ("
            "  tstzrange(starts_at, ends_at, '[)') WITH &&"
            ") WHERE (status NOT IN ('cancelled', 'no_show'))"
        )
    else:
        op.create_index(
            "ix_appointments_range",
            "appointments",
            ["starts_at", "ends_at"],
            unique=False,
        )


def downgrade() -> None:
    op.drop_table("appointments")
    op.drop_table("blocked_periods")
    op.drop_table("working_hours")
    op.drop_index(op.f("ix_services_code"), table_name="services")
    op.drop_table("services")
