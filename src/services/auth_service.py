import os
from datetime import datetime, timedelta
from typing import Annotated, Any, Union

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import get_db
from src.models.user_model import User

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT",
)


def create_access_token(
    subject: Union[
        str,
        Any,
    ],
    expires_delta: int = None,
) -> str:
    """
    Create a JWT token
    Args:
        subject (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """

    if expires_delta:
        expire = datetime.now() + timedelta(expires_delta)
    else:
        expire = datetime.now() + timedelta(
            minutes=float(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES"))
        )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ.get("JWT_SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM"),
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[
        str,
        Any,
    ],
    expires_delta: int = None,
) -> str:
    """
    Create a refresh token
    Args:
        subject (dict): data to be encoded
        expires_delta (timedelta | None, optional): expiration time. Defaults to None.
    Returns:
        str: JWT token
    """
    if expires_delta:
        expire = datetime.now() + timedelta(expires_delta)
    else:
        expire = datetime.now() + timedelta(
            minutes=float(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES"))
        )
    to_encode = {
        "exp": expire,
        "sub": str(subject),
    }
    encoded_jwt = jwt.encode(
        to_encode,
        os.environ.get("JWT_REFRESH_SECRET_KEY"),
        algorithm=os.environ.get("ALGORITHM"),
    )
    return encoded_jwt


async def verify_token(
    token: str,
):
    try:
        payload = jwt.decode(
            token,
            os.environ.get("JWT_SECRET_KEY"),
            algorithms=[os.environ.get("ALGORITHM")],
        )
        user = payload.get("sub")
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return user
    except (
        jwt.PyJWTError,
        ValueError,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )


async def authenticated(
    token: Annotated[str, Depends(reuseable_oauth)],
    db: AsyncSession = Depends(get_db),
):
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
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    return await db.get(User, user_id)
