from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.core.security import create_access_token, hash_password, verify_password
from app.models.users import User
from app.schemas.auth import LoginIn, RegisterIn, TokenOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenOut,
    description="Регистрация пользователя (только админ). Создаёт аккаунт и возвращает JWT-токен. Пароль хешируется.",
    dependencies=[Depends(require_admin)],
)
def register(payload: RegisterIn, db: Session = Depends(db_session)):
    exists = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(
        name=payload.name,
        lastname=payload.lastname,
        patronymic=payload.patronymic,
        age=payload.age,
        class_id=payload.class_id,
        phone_number=payload.phone_number,
        email=payload.email,
        created_at=__import__("datetime").date.today(),
        avatar_url=payload.avatar_url,
        user_rate=payload.user_rate,
        role_id=payload.role_id,
        is_complex=payload.is_complex,
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token)


@router.post(
    "/login",
    response_model=TokenOut,
    description="Аутентификация по email/паролю. Возвращает JWT-токен Bearer."
)
def login(payload: LoginIn, db: Session = Depends(db_session)):
    user = db.execute(select(User).where(User.email == payload.email)).scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token)


