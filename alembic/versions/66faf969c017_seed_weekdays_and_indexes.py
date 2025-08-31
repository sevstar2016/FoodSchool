"""seed weekdays and indexes

Revision ID: 66faf969c017
Revises: 7ccc2d561eb6
Create Date: 2025-08-28 19:11:28.191782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66faf969c017'
down_revision: Union[str, None] = '7ccc2d561eb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # индексы как в SQL-файле
    op.create_index('idx_users_login', 'users', ['login'], unique=False)
    op.create_index('idx_products_name', 'products', ['name'], unique=False)
    op.create_index('idx_orders_user_id', 'orders', ['user_id'], unique=False)
    op.create_index('idx_reviews_user_id', 'reviews', ['user_id'], unique=False)
    op.create_index('idx_complex_weekdays_complex_id', 'complex_weekdays', ['complex_id'], unique=False)
    op.create_index('idx_complex_weekdays_weekday_id', 'complex_weekdays', ['weekday_id'], unique=False)

    # сидирование дней недели (id автоинкремент, уникальное имя)
    weekdays = [
        {'name': 'Monday'},
        {'name': 'Tuesday'},
        {'name': 'Wednesday'},
        {'name': 'Thursday'},
        {'name': 'Friday'},
        {'name': 'Saturday'},
        {'name': 'Sunday'},
    ]
    conn = op.get_bind()
    for row in weekdays:
        conn.execute(sa.text("INSERT INTO weekdays(name) VALUES (:name) ON CONFLICT (name) DO NOTHING"), row)


def downgrade() -> None:
    conn = op.get_bind()
    # удаляем посеянные данные
    conn.execute(sa.text("DELETE FROM weekdays WHERE name IN ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday')"))

    # удаляем индексы
    op.drop_index('idx_complex_weekdays_weekday_id', table_name='complex_weekdays')
    op.drop_index('idx_complex_weekdays_complex_id', table_name='complex_weekdays')
    op.drop_index('idx_reviews_user_id', table_name='reviews')
    op.drop_index('idx_orders_user_id', table_name='orders')
    op.drop_index('idx_products_name', table_name='products')
    op.drop_index('idx_users_login', table_name='users')
