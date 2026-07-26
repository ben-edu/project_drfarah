"""Initial schema — bookings table (current state).

Revision ID: 0001
Revises: None
Create Date: 2026-07-26

This migration represents the current database schema. For staging
databases where this table already exists (from create_all()), stamp
this revision with `alembic stamp 0001` to mark it as already applied.
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("service_type", sa.String(length=128), nullable=False),
        sa.Column("visit_type", sa.String(length=128), nullable=False),
        sa.Column("preferred_day", sa.String(length=64), nullable=False),
        sa.Column("preferred_time", sa.String(length=32), nullable=False),
        sa.Column("time_window", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=128), nullable=False),
        sa.Column("last_name", sa.String(length=128), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=64), nullable=False),
        sa.Column("reason_category", sa.String(length=128), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="requested"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_bookings_id"), "bookings", ["id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_bookings_id"), table_name="bookings")
    op.drop_table("bookings")
