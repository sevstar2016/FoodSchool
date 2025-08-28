from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin, require_self_or_admin
from app.models.users import User
from app.schemas.users import UserCreate, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    response_model=UserOut,
    dependencies=[Depends(require_admin)],
    description="Создать пользователя (только админ)."
)
def create_user(payload: UserCreate, db: Session = Depends(db_session)):
    user = User(**payload.model_dump())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get(
    "/{user_id}",
    response_model=UserOut,
    description="Получить пользователя по id."
)
def get_user(user_id: int, db: Session = Depends(db_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(lambda user_id: require_self_or_admin(user_id))],
    description="Обновить пользователя. Разрешено админу или самому пользователю (например, сменить аватар)."
)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(db_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(user, k, v)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить пользователя (только админ)."
)
def delete_user(user_id: int, db: Session = Depends(db_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"status": "deleted"}


