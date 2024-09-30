from typing import (
    Optional,
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from src.models.user_model import (
    Role,
)


class UserSchema(BaseModel):
    id: int
    phone: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)
    role: Role


class UserCreateSchema(BaseModel):
    phone: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)
    password: str = Field(min_length=6)
    role: Role


class UserUpdateSchema(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]


class AuthData(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: str


class LoginData(BaseModel):
    phone: str
    password: str
