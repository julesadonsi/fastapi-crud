import os
from datetime import datetime, timedelta
from functools import wraps
from typing import Union, Any, Annotated
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

reuseable_oauth = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")

from sqlalchemy.orm import Session
from sqlalchemy.sql import Select
from typing import Optional


def create_access_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create a JWT token
    Args:
        subject (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """

    if expires_delta:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ.get("JWT_SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM"),
    )
    return encoded_jwt


def create_refresh_token(subject: Union[str, Any], expires_delta: int = None) -> str:
    """
    Create a refresh token
    Args:
        subject (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """
    to_encode = subject
    if expires_delta:
        expire = datetime.utcnow() + timedelta(expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=float(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ.get("JWT_REFRESH_SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM"),
    )
    return encoded_jwt


async def verify_token(token: str):
    try:
        payload = jwt.decode(
            token,
            os.environ.get("JWT_SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        print(payload)
        user = payload.get("sub")
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user
    except (jwt.PyJWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def get_current_user(token: Annotated[str, Depends(reuseable_oauth)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            os.environ.get("JWT_SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        user: str = payload.get("sub")
        if user is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    user: Annotated[User, Depends(get_current_user)],
):
    return user


def protected(func):
    @wraps(func)
    async def wrapper(*arg, **kwargs):
        user = get_current_active_user()
        return await func(user, *arg, **kwargs)

    return wrapper
