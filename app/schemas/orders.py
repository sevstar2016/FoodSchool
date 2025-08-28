from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class OrderBase(BaseModel):
    order_name: str
    user_id: int
    product_id: int
    created_at: datetime
    status_id: int


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    order_name: Optional[str] = None
    status_id: Optional[int] = None


class OrderOut(OrderBase):
    id: int

    class Config:
        from_attributes = True


