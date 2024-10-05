from pydantic import BaseModel, PositiveFloat
from sqlalchemy import create_engine

from src.schemas.user_shema import UserSchema


class ItemSchema(BaseModel):
    id: int
    name: str
    price: PositiveFloat
    user: UserSchema

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    name: str
    price: PositiveFloat
    quantity: PositiveFloat


class ItemUpdate(BaseModel):
    name: str | None = None
    price: PositiveFloat | None = None
    quantity: PositiveFloat | None = None
