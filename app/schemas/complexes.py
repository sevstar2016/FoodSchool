from datetime import date
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.products import ProductOut


class ComplexBase(BaseModel):
    name: str
    creation_date: date
    is_closed: bool


class ComplexCreate(ComplexBase):
    product_ids: List[int] = []
    weekday_ids: List[int] = []
    week_start: Optional[date] = None


class ComplexUpdate(BaseModel):
    name: Optional[str] = None
    creation_date: Optional[date] = None
    is_closed: Optional[bool] = None
    product_ids: Optional[List[int]] = None
    weekday_ids: Optional[List[int]] = None


class ComplexOut(ComplexBase):
    id: int
    products: List[ProductOut] = []

    class Config:
        from_attributes = True


class ChoiceItem(BaseModel):
    weekday_id: int
    complex_id: int


class ChoicesSetIn(BaseModel):
    items: List[ChoiceItem]



