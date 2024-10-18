from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/fastapi"

async_engine = create_async_engine(DATABASE_URL, pool_size=10, max_overflow=20)


async def get_db() -> AsyncSession:
    session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with session() as session:
        yield session
