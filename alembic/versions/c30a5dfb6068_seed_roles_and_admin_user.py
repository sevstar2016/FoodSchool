"""seed roles and admin user

Revision ID: c30a5dfb6068
Revises: 6c905aa6f122
Create Date: 2025-08-28 19:24:46.284472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.core.config import settings
from app.core.security import hash_password
from datetime import date

# revision identifiers, used by Alembic.
revision: str = 'c30a5dfb6068'
down_revision: Union[str, None] = '6c905aa6f122'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()

    # ensure roles
    admin_role_id = None
    user_role_id = None

    res = conn.execute(sa.text("SELECT id FROM users_roles WHERE name=:n"), {"n": "admin"}).first()
    if res:
        admin_role_id = res[0]
    else:
        admin_role_id = conn.execute(
            sa.text("INSERT INTO users_roles(name) VALUES (:n) RETURNING id"), {"n": "admin"}
        ).scalar_one()

    res = conn.execute(sa.text("SELECT id FROM users_roles WHERE name=:n"), {"n": "user"}).first()
    if res:
        user_role_id = res[0]
    else:
        user_role_id = conn.execute(
            sa.text("INSERT INTO users_roles(name) VALUES (:n) RETURNING id"), {"n": "user"}
        ).scalar_one()

    # ensure default class for admin
    class_id = None
    res = conn.execute(
        sa.text(
            "SELECT id FROM classes WHERE number=:num AND letter=:let AND year=:yr AND class_rate=:cr"
        ),
        {"num": 0, "let": "", "yr": 1970, "cr": 0},
    ).first()
    if res:
        class_id = res[0]
    else:
        class_id = conn.execute(
            sa.text(
                """
                INSERT INTO classes(number, letter, year, is_active, class_rate)
                VALUES (:num, :let, :yr, :ia, :cr)
                RETURNING id
                """
            ),
            {"num": 0, "let": "", "yr": 1970, "ia": True, "cr": 0},
        ).scalar_one()

    # ensure admin user
    admin_login = settings.admin_login
    admin_password = settings.admin_password
    admin_phone = settings.admin_phone
    admin_avatar_url = settings.admin_avatar_url

    res = conn.execute(sa.text("SELECT id FROM users WHERE login=:e"), {"e": admin_login}).first()
    if not res:
        conn.execute(
            sa.text(
                """
                INSERT INTO users(
                    name, lastname, patronymic, age, class_id, phone_number, login,
                    created_at, avatar_url, user_rate, role_id, is_complex, password_hash
                ) VALUES (
                    :name, :lastname, :patronymic, :age, :class_id, :phone_number, :login,
                    :created_at, :avatar_url, :user_rate, :role_id, :is_complex, :password_hash
                )
                """
            ),
            {
                "name": "Admin",
                "lastname": "User",
                "patronymic": "Adminovich",
                "age": 30,
                "class_id": class_id,
                "phone_number": admin_phone,
                "login": admin_login,
                "created_at": date.today(),
                "avatar_url": admin_avatar_url,
                "user_rate": 0,
                "role_id": admin_role_id,
                "is_complex": False,
                "password_hash": hash_password(admin_password),
            },
        )


def downgrade() -> None:
    conn = op.get_bind()
    # delete admin user
    conn.execute(sa.text("DELETE FROM users WHERE login=:e"), {"e": settings.admin_login})
    # try drop roles if no users reference
    # first set role_id of any users with these roles to NULL is not allowed, so only delete if unused
    conn.execute(sa.text("DELETE FROM users_roles WHERE name IN ('admin','user') AND id NOT IN (SELECT DISTINCT role_id FROM users)"))
