"""user complex choice

Revision ID: f3c282d68c7d
Revises: c30a5dfb6068
Create Date: 2025-08-28 19:33:46.928785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f3c282d68c7d'
down_revision: Union[str, None] = 'c30a5dfb6068'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_complex_choices',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('weekday_id', sa.Integer(), nullable=False),
        sa.Column('complex_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['complex_id'], ['complexes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['weekday_id'], ['weekdays.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('user_id', 'weekday_id'),
    )


def downgrade() -> None:
    op.drop_table('user_complex_choices')
