"""add created_by to videos

Revision ID: 0c7b0a6d4181
Revises: a4d9edd24066
Create Date: 2026-08-18 22:02:06.373728

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0c7b0a6d4181'
down_revision: Union[str, Sequence[str], None] = 'a4d9edd24066'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "videos",
        sa.Column(
            "created_by",
            sa.String(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "videos",
        "created_by",
    )

















