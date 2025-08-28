"""add week_start to user_complex_choices

Revision ID: e990144e89dd
Revises: f3c282d68c7d
Create Date: 2025-08-28 19:43:13.534552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'e990144e89dd'
down_revision: Union[str, None] = 'f3c282d68c7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_complex_choices', sa.Column('week_start', sa.Date(), nullable=False, server_default=sa.text('CURRENT_DATE')))


def downgrade() -> None:
    op.drop_column('user_complex_choices', 'week_start')
