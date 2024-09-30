from enum import (
    Enum,
)

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Float,
    Enum as SQLAEnum,
)
from sqlalchemy.orm import (
    Mapped,
)

from src.models.base_model import (
    Base,
)


class Role(Enum):
    ADMIN = "admin"
    USER = "user"
    OWNER = "owner"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    phone: Mapped[str] = Column(
        String,
        unique=True,
        index=True,
    )
    email: Mapped[str] = Column(
        String,
        unique=True,
        index=True,
        nullable=True,
    )
    password: Mapped[str] = Column(String)
    role: str = Column(
        SQLAEnum(Role),
        default=Role.USER,
    )
