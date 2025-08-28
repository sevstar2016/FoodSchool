from __future__ import annotations

from datetime import date
from typing import List, Optional

from sqlalchemy import Boolean, Date, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.db import Base


class UserRole(Base):
    __tablename__ = "users_roles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    users: Mapped[List[User]] = relationship("User", back_populates="role")


class Class(Base):
    __tablename__ = "classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    number: Mapped[Optional[int]] = mapped_column(Integer)
    letter: Mapped[Optional[str]] = mapped_column(String(255))
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False)
    class_rate: Mapped[int] = mapped_column(Integer, nullable=False)

    users: Mapped[List[User]] = relationship("User", back_populates="clazz")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[Optional[str]] = mapped_column(String(255))
    lastname: Mapped[Optional[str]] = mapped_column(String(255))
    patronymic: Mapped[str] = mapped_column(String(255), nullable=False)
    age: Mapped[int] = mapped_column(Integer, nullable=False)
    class_id: Mapped[int] = mapped_column(ForeignKey("classes.id"), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    avatar_url: Mapped[str] = mapped_column(Text, nullable=False)
    user_rate: Mapped[int] = mapped_column(Integer, nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("users_roles.id"), nullable=False)
    is_complex: Mapped[bool] = mapped_column(Boolean, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))

    clazz: Mapped[Class] = relationship("Class", back_populates="users")
    role: Mapped[UserRole] = relationship("UserRole", back_populates="users")


