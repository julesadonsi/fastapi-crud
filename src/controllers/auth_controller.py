from fastapi import APIRouter, Depends, HTTPException, status
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_

from src.db import get_db
from src.models.user import User
from src.schemas.user_shema import UserCreateSchema, UserSchema, AuthData, LoginData
from src.services.auth_service import (
    create_access_token,
    create_refresh_token,
    get_current_active_user,
)

auth_router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/signup", response_model=AuthData)
async def signup(
    data: UserCreateSchema, db: AsyncSession = Depends(get_db)
) -> AuthData:
    """
    Create a new user and return authentication token
    """
    existing_user = (
        await db.scalars(
            select(User).where(
                or_(User.email == data.email, User.username == data.username)
            )
        )
    ).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = pwd_context.encrypt(data.password)

    user = User(**data.model_dump())
    user.password = hashed_password
    db.add(user)

    await db.commit()
    await db.refresh(user)

    user_model = UserSchema(
        id=user.id, email=user.email, username=user.username, role=user.role
    )
    return AuthData(
        user=user_model,
        access_token=create_access_token(user_model.model_dump()),
        refresh_token=create_refresh_token(user_model.model_dump()),
    )


@auth_router.post("/login", response_model=AuthData)
async def login(data: LoginData, db: AsyncSession = Depends(get_db)) -> AuthData:
    """
    Authenticate a user and return authentication token
    """
    user = (await db.scalars(select(User).where(User.email == data.email))).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    if not pwd_context.verify(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    user_model = UserSchema(
        id=user.id, email=user.email, username=user.username, role=user.role
    )

    return AuthData(
        user=user_model,
        access_token=create_access_token(user_model.model_dump()),
        refresh_token=create_refresh_token(user_model.model_dump()),
    )


@auth_router.get("/me")
async def me(user: Session = Depends(get_current_active_user)):
    return user
