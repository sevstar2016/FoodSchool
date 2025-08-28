from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: str
    age: int
    class_id: int
    phone_number: str
    email: EmailStr
    created_at: date
    avatar_url: str
    user_rate: int
    role_id: int
    is_complex: bool


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str] = None
    lastname: Optional[str] = None
    patronymic: Optional[str] = None
    age: Optional[int] = None
    class_id: Optional[int] = None
    phone_number: Optional[str] = None
    avatar_url: Optional[str] = None
    user_rate: Optional[int] = None
    role_id: Optional[int] = None
    is_complex: Optional[bool] = None


class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


