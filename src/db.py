from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
    Session,
)

DATABASE_URL = "postgresql://postgres:root@localhost:5432/fastapi"

async_engine = create_engine(
    DATABASE_URL,
    echo=True,
    future=True,
)


def get_db() -> Session:
    session = sessionmaker(
        bind=async_engine,
        class_=Session,
        expire_on_commit=False,
    )
    with session() as session:
        yield session
