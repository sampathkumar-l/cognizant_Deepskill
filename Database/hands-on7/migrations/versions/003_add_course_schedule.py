"""add course schedule table

Revision ID: 003_add_course_schedule
Revises: 002_add_is_active
Create Date: 2026-07-12
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = "003_add_course_schedule"
down_revision = "002_add_is_active"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "course_schedules",

        sa.Column(
            "schedule_id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "course_id",
            sa.Integer(),
            sa.ForeignKey("courses.course_id"),
            nullable=False
        ),

        sa.Column(
            "day_of_week",
            sa.String(20),
            nullable=False
        ),

        sa.Column(
            "start_time",
            sa.Time(),
            nullable=False
        ),

        sa.Column(
            "end_time",
            sa.Time(),
            nullable=False
        )
    )


def downgrade():

    op.drop_table("course_schedules")