"""add duration to videos

Revision ID: a4d9edd24066
Revises: 
Create Date: 2026-08-18 21:24:36.421405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a4d9edd24066'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column(
        "videos",
        sa.Column(
            "duration",
            sa.Integer(),
            nullable=True,
        ),
    )



def downgrade():
    op.drop_column(
        "videos",
        "duration",
    )