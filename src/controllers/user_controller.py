from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import User
from src.schemas.user_shema import UserUpdateSchema, UserSchema
from src.services.auth_service import authenticated

user_router = APIRouter(prefix="/api/users", tags=["Users"])


@user_router.put("/{user_id}")
async def update_user(
    data: UserUpdateSchema,
    user_id: int,
    db: Session = Depends(get_db),
    user: AsyncSession = Depends(authenticated),
) -> UserSchema:
    try:
        user = db.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(user, key, value)
            db.commit()
        return UserSchema(id=user.id, phone=user.phone, email=user.email, role=user.role)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
