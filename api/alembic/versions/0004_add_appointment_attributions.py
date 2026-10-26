"""Add appointment_attributions table.

Revision ID: 0004
Revises: 0003
Create Date: 2026-10-26
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004"
down_revision: Union[str, None] = "0003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "appointment_attributions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("appointment_id", sa.Integer(), nullable=False),
        sa.Column("marketing_session_id", sa.String(length=64), nullable=True),
        sa.Column("first_touch", sa.JSON(), nullable=True),
        sa.Column("last_touch", sa.JSON(), nullable=True),
        sa.Column("partner_code", sa.String(length=128), nullable=True),
        sa.Column("traveler_segment", sa.String(length=16), nullable=False, server_default="unknown"),
        sa.Column("attribution_version", sa.String(length=16), nullable=False, server_default="v1"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["appointment_id"], ["appointments.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("appointment_id", name="uq_appointment_attributions_appointment_id"),
    )
    op.create_index(
        op.f("ix_appointment_attributions_appointment_id"),
        "appointment_attributions",
        ["appointment_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_appointment_attributions_marketing_session_id"),
        "appointment_attributions",
        ["marketing_session_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_appointment_attributions_marketing_session_id"),
        table_name="appointment_attributions",
    )
    op.drop_index(
        op.f("ix_appointment_attributions_appointment_id"),
        table_name="appointment_attributions",
    )
    op.drop_table("appointment_attributions")
