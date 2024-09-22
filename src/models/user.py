from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, DeclarativeBase
from sqlmodel import SQLModel

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = Column(String, unique=True, index=True)
    email: Mapped[str] = Column(String, unique=True, index=True)
    password: Mapped[str] = Column(String)
    role: Mapped[str] = Column(String, default="user")


class Token(Base):
    __tablename__ = "tokens"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    token: Mapped[str] = Column(String, index=True)
    user_id: Mapped[int] = Column(Integer, ForeignKey("users.id"))
