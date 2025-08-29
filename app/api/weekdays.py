from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session
from app.models.complexes import Weekday


router = APIRouter(prefix="/weekdays", tags=["weekdays"])


@router.get(
    "/",
    description="Справочник дней недели. Вернёт id и name для маппинга."
)
def list_weekdays(db: Session = Depends(db_session)):
    rows = db.scalars(select(Weekday)).all()
    return [{"id": w.id, "name": w.name} for w in rows]


