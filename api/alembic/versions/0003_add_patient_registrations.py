"""Add patient_registrations table.

Revision ID: 0003
Revises: 0002
Create Date: 2026-09-19
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "patient_registrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("public_reference", sa.String(length=32), nullable=False),
        sa.Column("resume_token_hash", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=24), nullable=False, server_default="draft"),
        sa.Column("appointment_reference", sa.String(length=64), nullable=True),
        sa.Column("first_name", sa.String(length=128), nullable=True),
        sa.Column("last_name", sa.String(length=128), nullable=True),
        sa.Column("date_of_birth", sa.Date(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("address_line1", sa.String(length=255), nullable=True),
        sa.Column("address_line2", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=True),
        sa.Column("state", sa.String(length=64), nullable=True),
        sa.Column("postal_code", sa.String(length=32), nullable=True),
        sa.Column("emergency_contact_name", sa.String(length=255), nullable=True),
        sa.Column("emergency_contact_phone", sa.String(length=64), nullable=True),
        sa.Column("privacy_acknowledged", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("public_reference"),
    )
    op.create_index(op.f("ix_patient_registrations_public_reference"), "patient_registrations", ["public_reference"], unique=True)
    op.create_index(op.f("ix_patient_registrations_status"), "patient_registrations", ["status"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_patient_registrations_status"), table_name="patient_registrations")
    op.drop_index(op.f("ix_patient_registrations_public_reference"), table_name="patient_registrations")
    op.drop_table("patient_registrations")
