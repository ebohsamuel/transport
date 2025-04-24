from datetime import datetime, timedelta, timezone
from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, status, Cookie
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app import database
from transport_app.crud import crud_user
from transport_app.schemas import schemas_user, schemas_token
from fastapi.templating import Jinja2Templates
import os

template = Jinja2Templates(directory="transport_app/template")


SECRET_KEY = "ec74be764e3ff9ca044d6b13094bbcfad3c70e190410c01c233b0428a5ce67a5"
ALGORITHM = "HS256"


async def get_db():
    async with database.async_SessionLocal() as session:
        yield session


async def authenticate_user(db: AsyncSession, email: str, password: str):
    user_data = await crud_user.get_user_by_email(db, email)
    if not user_data:
        return False
    if not crud_user.pwd_context.verify(password, user_data.hashed_password):
        return False
    return user_data


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(access_token: str = Cookie(), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = access_token[len("Bearer "):]

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas_token.TokenData(username=email)
    except ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    user_data = await crud_user.get_user_by_email(db, email=token_data.username)
    if user_data is None:
        raise credentials_exception
    return user_data


async def get_current_active_user(current_user: Annotated[schemas_user.User, Depends(get_current_user)]):
    if current_user.status != "active":
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_manager(user: schemas_user.UserCreate = Depends(get_current_active_user)):
    if user.role != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions.")
    return user


async def check_accountant(user: schemas_user.UserCreate = Depends(get_current_active_user)):
    if user.role != 'accountant':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions.")
    return user

