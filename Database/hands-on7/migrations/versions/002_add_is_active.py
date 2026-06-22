"""add is_active to students

Revision ID: 002_add_is_active
Revises: 001_initial_schema
Create Date: 2026-07-12

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "002_add_is_active"
down_revision = "001_initial_schema"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "students",
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.true()
        )
    )


def downgrade():
    op.drop_column("students", "is_active")