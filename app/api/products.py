from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.models.models import Product
from app.schemas.products import ProductCreate, ProductOut, ProductUpdate

router = APIRouter(prefix="/products", tags=["products"])


@router.post(
    "/",
    response_model=ProductOut,
    dependencies=[Depends(require_admin)],
    description="Создать продукт (только админ)."
)
def create_product(payload: ProductCreate, db: Session = Depends(db_session)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get(
    "/{product_id}",
    response_model=ProductOut,
    description="Получить продукт по id."
)
def get_product(product_id: int, db: Session = Depends(db_session)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put(
    "/{product_id}",
    response_model=ProductOut,
    dependencies=[Depends(require_admin)],
    description="Обновить продукт (только админ)."
)
def update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(db_session)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(product, k, v)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить продукт (только админ)."
)
def delete_product(product_id: int, db: Session = Depends(db_session)):
    product = db.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"status": "deleted"}


