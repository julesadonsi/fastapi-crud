from fastapi import APIRouter, Depends, HTTPException, status
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import User
from src.schemas.user_shema import UserCreateSchema, UserSchema, AuthData, LoginData
from src.services.auth_service import (
    create_access_token,
    create_refresh_token,
    authenticated,
)

auth_router = APIRouter(
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@auth_router.post("/signup", response_model=AuthData)
async def signup(data: UserCreateSchema, db: Session = Depends(get_db)) -> AuthData:
    """
    Create a new user and return authentication token
    """
    existing_user = db.query(User).filter_by(phone=data.phone).first()
    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="User already exists"
        )
    hashed_password = pwd_context.encrypt(data.password)

    user = User(**data.model_dump())
    user.password = hashed_password

    db.add(user)
    db.commit()
    db.refresh(user)

    user_model = UserSchema(
        id=user.id, email=user.email, phone=user.phone, role=user.role
    )
    return AuthData(
        user=user_model,
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@auth_router.post("/login", response_model=AuthData)
async def login(data: LoginData, db: Session = Depends(get_db)) -> AuthData:
    """
    Authenticate a user and return authentication token
    """
    user = db.query(User).filter_by(phone=data.phone).first()
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
        id=user.id, email=user.email, phone=user.phone, role=user.role
    )

    return AuthData(
        user=user_model,
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@auth_router.get("/me")
async def me(user: Session = Depends(authenticated)):
    return vars(user)
