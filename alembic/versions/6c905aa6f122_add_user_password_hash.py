"""add user password_hash

Revision ID: 6c905aa6f122
Revises: 66faf969c017
Create Date: 2025-08-28 19:20:35.247775

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c905aa6f122'
down_revision: Union[str, None] = '66faf969c017'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('password_hash', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'password_hash')
