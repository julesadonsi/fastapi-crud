from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:root@localhost:5432/fastapi"

engine = AsyncEngine(create_engine(DATABASE_URL, echo=True, future=True))


async def init_db():
    async with engine.begin() as conn:
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_db() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session
