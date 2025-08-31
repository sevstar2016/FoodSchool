from pydantic import BaseModel


class RegisterIn(BaseModel):
    login: str
    name: str | None = None
    lastname: str | None = None
    patronymic: str
    age: int
    class_id: int
    phone_number: str
    password: str
    avatar_url: str
    user_rate: int
    role_id: int
    is_complex: bool


class LoginIn(BaseModel):
    login: str
    password: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChangePasswordIn(BaseModel):
    current_password: str
    new_password: str


