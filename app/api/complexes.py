from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from datetime import date, timedelta

from app.api.deps import db_session, get_current_user, require_admin
from app.models.complexes import Complex, ComplexProduct, ComplexWeekday, Weekday, UserComplexChoice
from app.models.products import Product
from app.schemas.complexes import ComplexCreate, ComplexOut, ComplexUpdate, ChoicesSetIn
from app.models.users import User

router = APIRouter(prefix="/complexes", tags=["complexes"])


@router.post(
    "/",
    response_model=ComplexOut,
    dependencies=[Depends(require_admin)],
    description="Создать комплекс (только админ). Можно указать продукты и дни недели."
)
def create_complex(payload: ComplexCreate, db: Session = Depends(db_session)):
    complex_obj = Complex(
        name=payload.name,
        creation_date=payload.creation_date,
        is_closed=payload.is_closed,
    )
    db.add(complex_obj)
    db.flush()

    for pid in payload.product_ids:
        db.add(ComplexProduct(complex_id=complex_obj.id, product_id=pid))
    for wid in payload.weekday_ids:
        db.add(ComplexWeekday(complex_id=complex_obj.id, weekday_id=wid))

    db.commit()
    db.refresh(complex_obj)
    return complex_obj


@router.get(
    "/{complex_id}",
    response_model=ComplexOut,
    description="Получить комплекс по id."
)
def get_complex(complex_id: int, db: Session = Depends(db_session)):
    obj = db.get(Complex, complex_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complex not found")
    return obj


@router.put(
    "/{complex_id}",
    response_model=ComplexOut,
    dependencies=[Depends(require_admin)],
    description="Обновить комплекс (только админ). Обновляет связи с продуктами и днями."
)
def update_complex(complex_id: int, payload: ComplexUpdate, db: Session = Depends(db_session)):
    obj = db.get(Complex, complex_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complex not found")

    data = payload.model_dump(exclude_unset=True)
    product_ids = data.pop("product_ids", None)
    weekday_ids = data.pop("weekday_ids", None)

    for k, v in data.items():
        setattr(obj, k, v)
    db.add(obj)
    db.flush()

    if product_ids is not None:
        db.execute(delete(ComplexProduct).where(ComplexProduct.complex_id == obj.id))
        for pid in product_ids:
            db.add(ComplexProduct(complex_id=obj.id, product_id=pid))

    if weekday_ids is not None:
        db.execute(delete(ComplexWeekday).where(ComplexWeekday.complex_id == obj.id))
        for wid in weekday_ids:
            db.add(ComplexWeekday(complex_id=obj.id, weekday_id=wid))

    db.commit()
    db.refresh(obj)
    return obj


@router.delete(
    "/{complex_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить комплекс (только админ)."
)
def delete_complex(complex_id: int, db: Session = Depends(db_session)):
    obj = db.get(Complex, complex_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complex not found")
    db.delete(obj)
    db.commit()
    return {"status": "deleted"}


def _next_monday(today: date) -> date:
    return today + timedelta(days=((7 - today.weekday()) % 7))

def _current_monday(today: date) -> date:
    return today - timedelta(days=today.weekday())


@router.get(
    "/week/next",
    description="Получить комплексы на следующую неделю, сгруппированные по weekday_id (1..7)."
)
def get_next_week_complexes(db: Session = Depends(db_session), user: User = Depends(get_current_user)):
    rows = db.execute(
        select(ComplexWeekday.weekday_id, Complex)
        .join(Complex, Complex.id == ComplexWeekday.complex_id)
        .where(Complex.is_closed == False)
    ).all()
    result: dict[int, list[ComplexOut]] = {}
    for weekday_id, complex_obj in rows:
        result.setdefault(weekday_id, []).append(ComplexOut.model_validate(complex_obj))
    return result


@router.get(
    "/week/current",
    description="Получить комплексы на текущую неделю, сгруппированные по weekday_id (1..7)."
)
def get_current_week_complexes(db: Session = Depends(db_session), user: User = Depends(get_current_user)):
    rows = db.execute(
        select(ComplexWeekday.weekday_id, Complex)
        .join(Complex, Complex.id == ComplexWeekday.complex_id)
        .where(Complex.is_closed == False)
    ).all()
    result: dict[int, list[ComplexOut]] = {}
    for weekday_id, complex_obj in rows:
        result.setdefault(weekday_id, []).append(ComplexOut.model_validate(complex_obj))
    return result


@router.post(
    "/week/next/choices",
    description="Выбрать комплексы по дням следующей недели (перезаписывает выбор)."
)
def set_next_week_choices(payload: ChoicesSetIn, db: Session = Depends(db_session), user: User = Depends(get_current_user)):
    week_start = _next_monday(date.today())
    db.execute(
        delete(UserComplexChoice).where(
            UserComplexChoice.user_id == user.id,
            UserComplexChoice.week_start == week_start,
        )
    )
    for item in payload.items:
        if not db.get(Weekday, item.weekday_id) or not db.get(Complex, item.complex_id):
            raise HTTPException(status_code=400, detail="Invalid weekday or complex")
        db.add(
            UserComplexChoice(
                user_id=user.id,
                weekday_id=item.weekday_id,
                complex_id=item.complex_id,
                week_start=week_start,
            )
        )
    db.commit()
    return {"status": "saved", "week_start": str(week_start)}


@router.get(
    "/week/next/choices",
    description="Получить текущий выбор комплексов пользователя на следующую неделю."
)
def get_next_week_choices(db: Session = Depends(db_session), user: User = Depends(get_current_user)):
    week_start = _next_monday(date.today())
    items = db.execute(
        select(UserComplexChoice.weekday_id, UserComplexChoice.complex_id)
        .where(
            UserComplexChoice.user_id == user.id,
            UserComplexChoice.week_start == week_start,
        )
    ).all()
    return {"week_start": str(week_start), "items": [{"weekday_id": w, "complex_id": c} for w, c in items]}


@router.get(
    "/week/current/choices",
    description="Получить текущий выбор комплексов пользователя на текущую неделю."
)
def get_current_week_choices(db: Session = Depends(db_session), user: User = Depends(get_current_user)):
    week_start = _current_monday(date.today())
    items = db.execute(
        select(UserComplexChoice.weekday_id, UserComplexChoice.complex_id)
        .where(
            UserComplexChoice.user_id == user.id,
            UserComplexChoice.week_start == week_start,
        )
    ).all()
    return {"week_start": str(week_start), "items": [{"weekday_id": w, "complex_id": c} for w, c in items]}


@router.patch(
    "/{complex_id}/close",
    dependencies=[Depends(require_admin)],
    description="Установить флаг is_closed для комплекса (только админ). Если true — комплекс не возвращается в API."
)
def set_complex_closed(complex_id: int, is_closed: bool, db: Session = Depends(db_session)):
    obj = db.get(Complex, complex_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Complex not found")
    obj.is_closed = is_closed
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return {"id": obj.id, "is_closed": obj.is_closed}


