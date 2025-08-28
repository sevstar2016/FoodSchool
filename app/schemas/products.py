from typing import Optional

from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    blc: int
    mass: int
    rate: int
    picture_url: str
    price: float
    compound: str
    is_hidden: bool
    is_complex: bool
    product_type_id: int


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    blc: Optional[int] = None
    mass: Optional[int] = None
    rate: Optional[int] = None
    picture_url: Optional[str] = None
    price: Optional[float] = None
    compound: Optional[str] = None
    is_hidden: Optional[bool] = None
    is_complex: Optional[bool] = None
    product_type_id: Optional[int] = None


class ProductOut(ProductBase):
    id: int

    class Config:
        from_attributes = True


