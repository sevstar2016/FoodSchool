"""add complexes.is_closed

Revision ID: 89e8b2e7f88d
Revises: e990144e89dd
Create Date: 2025-08-29 12:37:44.386549

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '89e8b2e7f88d'
down_revision: Union[str, None] = 'e990144e89dd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # add complexes.is_closed with default false for existing rows, then drop server_default
    op.add_column('complexes', sa.Column('is_closed', sa.Boolean(), nullable=False, server_default=sa.text('false')))
    op.alter_column('complexes', 'is_closed', server_default=None)


def downgrade() -> None:
    op.drop_column('complexes', 'is_closed')
