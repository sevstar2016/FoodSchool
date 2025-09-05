from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import db_session, require_admin
from app.models.products import ProductType
from app.schemas.products import ProductTypeCreate, ProductTypeOut, ProductTypeUpdate

router = APIRouter(prefix="/product-types", tags=["product-types"])


@router.get(
    "/",
    response_model=List[ProductTypeOut],
    description="Получить все типы продуктов."
)
def get_product_types(db: Session = Depends(db_session)):
    return db.execute(select(ProductType)).scalars().all()


@router.get(
    "/{product_type_id}",
    response_model=ProductTypeOut,
    description="Получить тип продукта по id."
)
def get_product_type(product_type_id: int, db: Session = Depends(db_session)):
    product_type = db.get(ProductType, product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    return product_type


@router.post(
    "/",
    response_model=ProductTypeOut,
    dependencies=[Depends(require_admin)],
    description="Создать тип продукта (только админ)."
)
def create_product_type(payload: ProductTypeCreate, db: Session = Depends(db_session)):
    product_type = ProductType(**payload.model_dump())
    db.add(product_type)
    db.commit()
    db.refresh(product_type)
    return product_type


@router.put(
    "/{product_type_id}",
    response_model=ProductTypeOut,
    dependencies=[Depends(require_admin)],
    description="Обновить тип продукта (только админ)."
)
def update_product_type(product_type_id: int, payload: ProductTypeUpdate, db: Session = Depends(db_session)):
    product_type = db.get(ProductType, product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(product_type, k, v)
    db.add(product_type)
    db.commit()
    db.refresh(product_type)
    return product_type


@router.delete(
    "/{product_type_id}",
    dependencies=[Depends(require_admin)],
    description="Удалить тип продукта (только админ)."
)
def delete_product_type(product_type_id: int, db: Session = Depends(db_session)):
    product_type = db.get(ProductType, product_type_id)
    if not product_type:
        raise HTTPException(status_code=404, detail="Product type not found")
    db.delete(product_type)
    db.commit()
    return {"status": "deleted"}