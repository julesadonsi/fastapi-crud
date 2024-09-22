from sqlalchemy import Integer, Column, Float, String
from sqlalchemy.orm import Mapped

from src.models.base import Base


class Item(Base):
    __tablename__ = "items"
    id: Mapped[int] = Column(Integer, primary_key=True)
    name: Mapped[str] = Column(String)
    price: Mapped[float] = Column(Float)
    quantity: Mapped[int] = Column(Integer)
