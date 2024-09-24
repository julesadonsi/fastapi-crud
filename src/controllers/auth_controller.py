from fastapi import APIRouter, Depends, HTTPException, status, Response
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from starlette.responses import Response

from src.db import get_db
from src.models.user import User
from src.schemas.user_shema import UserCreateSchema, UserSchema, AuthData, LoginData
from passlib.apps import custom_app_context as pwd_context

from src.services.auth_service import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_current_active_user,
)

auth_router = APIRouter()


@auth_router.post("/signup", response_model=AuthData)
async def signup(data: UserCreateSchema, db: Session = Depends(get_db)) -> AuthData:
    """
    Create a new user and return authentication token
    """
    query = select(User).filter_by(email=data.email)
    existing_user = await db.execute(query)
    if existing_user.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = pwd_context.encrypt(data.password)

    user = User(**data.model_dump())
    user.password = hashed_password
    db.add(user)
    await db.commit()
    user_model = UserSchema(
        id=user.id, email=user.email, username=user.username, role=user.role
    )
    return AuthData(
        user=user_model,
        access_token=create_access_token(user_model.model_dump()),
        refresh_token=create_refresh_token(user_model.model_dump()),
    )


@auth_router.post("/login")
async def login(data: LoginData, db: Session = Depends(get_db)) -> AuthData:
    """
    Authenticate a user and return authentication token
    """
    user_result = await db.execute(select(User).where(data.email == User.email))
    user = user_result.scalar_one_or_none()
    if not user:
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
