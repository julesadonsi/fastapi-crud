from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.services.auth_service import authenticated


def transform_dict(obj):
    data = vars(obj).copy()
    for key, value in data.items():
        if isinstance(value, list):
            data[key] = [vars(v) for v in value]
        elif hasattr(value, "__dict__"):
            data[key] = vars(value)
    return data


def combine_dependencies(
    database: AsyncSession = Depends(get_db), user: AsyncSession = Depends(authenticated)
) -> tuple[AsyncSession, AsyncSession]:
    return database, user
