from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user import User
from src.schemas.user_shema import UserUpdateSchema, UserSchema
from src.services.auth_service import get_current_active_user

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.put("/{user_id}")
async def update_user(
    data: UserUpdateSchema,
    user_id: int,
    db: AsyncSession = Depends(get_db),
    user: AsyncSession = Depends(get_current_active_user),
) -> UserSchema:
    try:
        user = await db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(user, key, value)
            await db.commit()
        return UserSchema(
            id=user.id, username=user.username, email=user.email, role=user.role
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
