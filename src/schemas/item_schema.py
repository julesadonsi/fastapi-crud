from pydantic import BaseModel, PositiveFloat

from src.schemas.user_shema import UserSchema


class ItemSchema(BaseModel):
    id: int
    name: str
    price: PositiveFloat
    quantity: PositiveFloat
    user: UserSchema

    class Config:
        from_attributes = True


class ItemCreate(BaseModel):
    name: str
    price: PositiveFloat
    quantity: PositiveFloat

    class Config:
        from_attributes = True


class ItemUpdate(BaseModel):
    name: str | None = None
    price: PositiveFloat | None = None
    quantity: PositiveFloat | None = None

    class Config:
        from_attributes = True
