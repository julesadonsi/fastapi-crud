from sqlalchemy import table
from sqlmodel import Field, SQLModel
from typing import Optional


class Item(SQLModel):

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    price: str
    quantity: int
