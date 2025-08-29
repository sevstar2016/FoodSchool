from typing import Optional, List

from pydantic import BaseModel


class ClassBase(BaseModel):
    number: Optional[int] = None
    letter: Optional[str] = None
    year: int
    is_active: bool
    class_rate: int


class ClassCreate(ClassBase):
    pass


class ClassUpdate(BaseModel):
    number: Optional[int] = None
    letter: Optional[str] = None
    year: Optional[int] = None
    is_active: Optional[bool] = None
    class_rate: Optional[int] = None


class ClassOut(ClassBase):
    id: int

    class Config:
        from_attributes = True


class ClassAddStudentsIn(BaseModel):
    user_ids: List[int]


