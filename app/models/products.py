from __future__ import annotations

from typing import List

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class ProductType(Base):
    __tablename__ = "product_types"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    products: Mapped[List["Product"]] = relationship("Product", back_populates="type")


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    blc: Mapped[int] = mapped_column(Integer, nullable=False)
    mass: Mapped[int] = mapped_column(Integer, nullable=False)
    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    picture_url: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    compound: Mapped[str] = mapped_column(Text, nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_complex: Mapped[bool] = mapped_column(Boolean, nullable=False)
    product_type_id: Mapped[int] = mapped_column(ForeignKey("product_types.id"), nullable=False)

    type: Mapped[ProductType] = relationship("ProductType", back_populates="products")


