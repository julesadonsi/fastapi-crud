import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.config import AVATAR_DIR, ROOT_DIR
from src.db import get_db
from src.models.user_model import User
from src.schemas.user_shema import UpdateAvatarSchema, UserSchema, UserUpdateSchema
from src.services.auth_service import authenticated
from src.utilis.transform import combine_dependencies

user_router = APIRouter(prefix="/users", tags=["users"])


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
        return UserSchema(id=user.id, phone=user.phone, email=user.email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@user_router.patch("/{user_id}/avatar", response_model=UserSchema)
async def update_avatar(
    user_id: int,
    avatar: UploadFile = File(...),
    dependencies: tuple[AsyncSession, AsyncSession] = Depends(combine_dependencies),
):
    database, user = dependencies
    wanted_user = await database.get(User, user_id)

    _, extension = os.path.splitext(avatar.filename)
    new_filename = f"avatar_{wanted_user.id}{extension}"
    file_path = AVATAR_DIR / new_filename

    if wanted_user.avatar:
        if Path(str(wanted_user.avatar)).exists():
            Path(str(wanted_user.avatar)).unlink()

    with open(file_path, "wb") as buffer:
        buffer.write(await avatar.read())
    wanted_user.avatar = str(file_path.relative_to(ROOT_DIR))

    database.add(wanted_user)
    await database.commit()
    await database.refresh(wanted_user)
    return UserSchema.model_validate(wanted_user)
