from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: int
    username: str = Field(min_length=3)
    email: EmailStr
    role: str


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=6)
    role: str


class UserUpdateSchema(BaseModel):
    username: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]


class AuthData(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: str


class LoginData(BaseModel):
    email: EmailStr
    password: str
