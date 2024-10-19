from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import User
from src.schemas.user_shema import (
    AuthenticatedUser,
    UserCreateSchema,
    UserSchema,
    AuthData,
    LoginData,
)
from src.services.auth_service import (
    create_access_token,
    create_refresh_token,
    authenticated,
)

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/signup", response_model=AuthData)
async def signup(data: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    """
    Create a new user and return authentication token
    """

    query = await db.execute(select(User).filter_by(phone=data.phone))
    user = query.scalars().first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = pwd_context.hash(data.password)

    user = User(**data.model_dump())
    user.password = hashed_password

    db.add(user)
    await db.commit()
    await db.refresh(user)

    user_model = UserSchema.model_validate(user)
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "user": user_model,
    }


@auth_router.post("/login")
async def login(data: LoginData, db: AsyncSession = Depends(get_db)):
    """
    Authenticate a user and return authentication token
    """
    query = await db.execute(select(User).filter_by(phone=data.phone))
    user = query.scalars().first()
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
    user_schema = UserSchema.model_validate(user)

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "user": user_schema,
    }


@auth_router.get("/me")
async def me(user: Session = Depends(authenticated)):
    return AuthenticatedUser(**vars(user))
