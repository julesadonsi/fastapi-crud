from enum import Enum
from typing import List

from sqlalchemy import Column, Integer, String, ForeignKey, Float, Enum as SQLAEnum
from sqlalchemy.orm import Mapped, relationship

from src.models.base_model import Base


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    OWNER = "owner"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    phone: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True, nullable=True)
    password: Mapped[str] = Column(String)
    role: str = Column(SQLAEnum(Role), default=Role.USER)
    items: Mapped[List["Item"]] = relationship(back_populates="user")


class Item(Base):
    __tablename__ = "items"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String)
    price: Mapped[float] = Column(Float)
    quantity: Mapped[int] = Column(Integer)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(
        User, back_populates="items", foreign_keys=[user_id]
    )
