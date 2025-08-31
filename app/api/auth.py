from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin, get_current_user
from app.core.security import create_access_token, hash_password, verify_password
from app.models.users import User
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import LoginIn, RegisterIn, TokenOut, ChangePasswordIn
from app.schemas.users import UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=TokenOut,
    description="Регистрация пользователя (только админ). Создаёт аккаунт и возвращает JWT-токен. Пароль хешируется.",
    dependencies=[Depends(require_admin)],
)
def register(payload: RegisterIn, db: Session = Depends(db_session)):
    exists = db.execute(select(User).where((User.login == payload.login))).scalar_one_or_none()
    if exists:
        raise HTTPException(status_code=400, detail="Login already registered")

    user = User(
        login=payload.login,
        name=payload.name,
        lastname=payload.lastname,
        patronymic=payload.patronymic,
        age=payload.age,
        class_id=payload.class_id,
        phone_number=payload.phone_number,
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
    description="Аутентификация по логину/паролю. Возвращает JWT-токен Bearer. Поддерживает OAuth2PasswordRequestForm.",
)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(db_session)):
    user = db.execute(select(User).where(User.login == form.username)).scalar_one_or_none()
    if not user or not user.password_hash or not verify_password(form.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(str(user.id))
    return TokenOut(access_token=token)


@router.get(
    "/me",
    response_model=UserOut,
    description="Вернуть профиль текущего авторизованного пользователя."
)
def me(current = Depends(get_current_user)):
    return current


@router.post(
    "/change-password",
    description="Смена пароля текущего пользователя. Требует указать текущий и новый пароли."
)
def change_password(payload: ChangePasswordIn, current = Depends(get_current_user), db: Session = Depends(db_session)):
    if not current.password_hash or not verify_password(payload.current_password, current.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current.password_hash = hash_password(payload.new_password)
    db.add(current)
    db.commit()
    return {"status": "changed"}


