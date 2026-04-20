"""add post_voted notification type

Revision ID: d2debbefd4d6
Revises: be582912f6b0
Create Date: 2026-04-21 04:06:27.071601

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2debbefd4d6'
down_revision: Union[str, Sequence[str], None] = 'be582912f6b0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("ALTER TYPE notification_type ADD VALUE IF NOT EXISTS 'post_voted'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values without recreating the type
    pass
