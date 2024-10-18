from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: int
    phone: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)


class UserCreateSchema(BaseModel):
    phone: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)
    password: str = Field(min_length=6)


class UserUpdateSchema(BaseModel):
    phone: Optional[str]
    email: Optional[EmailStr]


class AuthData(BaseModel):
    user: UserSchema
    access_token: str
    refresh_token: str


class LoginData(BaseModel):
    phone: str
    password: str


class AuthenticatedUser(BaseModel):
    id: int
    phone: str
    email: EmailStr
