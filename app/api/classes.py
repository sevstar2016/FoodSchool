from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.models.users import Class as ClassModel, User
from app.schemas.classes import ClassCreate, ClassOut, ClassUpdate, ClassAddStudentsIn


router = APIRouter(prefix="/classes", tags=["classes"])


@router.post(
    "/",
    response_model=ClassOut,
    dependencies=[Depends(require_admin)],
    description="Создать класс (только админ)."
)
def create_class(payload: ClassCreate, db: Session = Depends(db_session)):
    obj = ClassModel(**payload.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.get(
    "/{class_id}",
    response_model=ClassOut,
    description="Получить класс по id."
)
def get_class(class_id: int, db: Session = Depends(db_session)):
    obj = db.get(ClassModel, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return obj


@router.get(
    "/",
    response_model=list[ClassOut],
    description="Получить список всех классов."
)
def list_classes(db: Session = Depends(db_session)):
    return db.scalars(select(ClassModel)).all()


@router.put(
    "/{class_id}",
    response_model=ClassOut,
    dependencies=[Depends(require_admin)],
    description="Обновить класс (только админ)."
)
def update_class(class_id: int, payload: ClassUpdate, db: Session = Depends(db_session)):
    obj = db.get(ClassModel, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Class not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@router.delete(
    "/{class_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить класс (только админ)."
)
def delete_class(class_id: int, db: Session = Depends(db_session)):
    obj = db.get(ClassModel, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Class not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}


@router.post(
    "/{class_id}/students",
    dependencies=[Depends(require_admin)],
    description="Добавить перечисленных учеников в класс (только админ)."
)
def add_students(class_id: int, payload: ClassAddStudentsIn, db: Session = Depends(db_session)):
    obj = db.get(ClassModel, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Class not found")
    users = db.scalars(select(User).where(User.id.in_(payload.user_ids))).all()
    for u in users:
        u.class_id = class_id
        db.add(u)
    db.commit()
    return {"status": "added", "count": len(users)}


@router.delete(
    "/{class_id}/students/{user_id}",
    dependencies=[Depends(require_admin)],
    description="Исключить ученика из класса (только админ). Требуется указать целевой класс через параметр to_class_id, иначе вернётся 400."
)
def remove_student(
    class_id: int,
    user_id: int,
    to_class_id: int | None = None,
    db: Session = Depends(db_session),
):
    cls = db.get(ClassModel, class_id)
    if not cls:
        raise HTTPException(status_code=404, detail="Class not found")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.class_id != class_id:
        raise HTTPException(status_code=400, detail="User is not in this class")
    if to_class_id is None:
        # class_id в схеме NOT NULL, поэтому нужен целевой класс
        raise HTTPException(status_code=400, detail="to_class_id is required to reassign student")
    target = db.get(ClassModel, to_class_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target class not found")
    user.class_id = to_class_id
    db.add(user)
    db.commit()
    return {"status": "moved", "user_id": user_id, "from": class_id, "to": to_class_id}


