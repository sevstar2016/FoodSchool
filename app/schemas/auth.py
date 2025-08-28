from pydantic import BaseModel, EmailStr


class RegisterIn(BaseModel):
    name: str | None = None
    lastname: str | None = None
    patronymic: str
    age: int
    class_id: int
    phone_number: str
    email: EmailStr
    password: str
    avatar_url: str
    user_rate: int
    role_id: int
    is_complex: bool


class LoginIn(BaseModel):
    email: EmailStr
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


