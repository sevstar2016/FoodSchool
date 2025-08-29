from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.models.orders import Order
from app.schemas.orders import OrderCreate, OrderOut, OrderUpdate

router = APIRouter(prefix="/orders", tags=["orders"])


@router.post(
    "/",
    response_model=OrderOut,
    dependencies=[Depends(require_admin)],
    description="Создать заказ (только админ)."
)
def create_order(payload: OrderCreate, db: Session = Depends(db_session)):
    order = Order(**payload.model_dump())
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get(
    "/",
    response_model=List[OrderOut],
    description="Получить все заказы."
)
def get_orders(db: Session = Depends(db_session)):
    return db.execute(select(Order)).scalars().all()

@router.get(
    "/{order_id}",
    response_model=OrderOut,
    description="Получить заказ по id."
)
def get_order(order_id: int, db: Session = Depends(db_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.put(
    "/{order_id}",
    response_model=OrderOut,
    dependencies=[Depends(require_admin)],
    description="Обновить заказ (только админ)."
)
def update_order(order_id: int, payload: OrderUpdate, db: Session = Depends(db_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(order, k, v)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.delete(
    "/{order_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить заказ (только админ)."
)
def delete_order(order_id: int, db: Session = Depends(db_session)):
    order = db.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"status": "deleted"}


