from typing import Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserSchema(BaseModel):
    id: int
    phone: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)
    avatar: str

    class Config:
        from_attributes = True


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

    class Config:
        from_attributes = True


class LoginData(BaseModel):
    phone: str
    password: str


class AuthenticatedUser(BaseModel):
    id: int
    phone: str
    email: EmailStr


class UpdateAvatarSchema(BaseModel):
    avatar: UploadFile = File(...)

    @field_validator("avatar")
    def check_avatar(cls, v):
        if v is None:
            raise ValueError("Avatar cannot be None")
        return v
