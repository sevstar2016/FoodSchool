from __future__ import annotations

from datetime import date
from typing import List

from sqlalchemy import Boolean, ForeignKey, Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class Complex(Base):
    __tablename__ = "complexes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)


class UserComplexChoice(Base):
    __tablename__ = "user_complex_choices"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    weekday_id: Mapped[int] = mapped_column(ForeignKey("weekdays.id", ondelete="CASCADE"), primary_key=True)
    complex_id: Mapped[int] = mapped_column(ForeignKey("complexes.id", ondelete="CASCADE"), nullable=False)
    week_start: Mapped[date] = mapped_column(Date, nullable=False, default=date.today)
    is_closed: Mapped[bool] = mapped_column(Boolean, nullable=False)


class UserComplex(Base):
    __tablename__ = "user_complexes"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    complex_id: Mapped[int] = mapped_column(ForeignKey("complexes.id", ondelete="CASCADE"), primary_key=True)


class ComplexProduct(Base):
    __tablename__ = "complex_products"

    complex_id: Mapped[int] = mapped_column(ForeignKey("complexes.id", ondelete="CASCADE"), primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), primary_key=True)


class Weekday(Base):
    __tablename__ = "weekdays"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)


class ComplexWeekday(Base):
    __tablename__ = "complex_weekdays"

    complex_id: Mapped[int] = mapped_column(ForeignKey("complexes.id", ondelete="CASCADE"), primary_key=True)
    weekday_id: Mapped[int] = mapped_column(ForeignKey("weekdays.id", ondelete="RESTRICT"), primary_key=True)


