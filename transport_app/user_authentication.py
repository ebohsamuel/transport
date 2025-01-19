from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.orm import Session
import jwt
from fastapi import Depends, HTTPException, status, Request, Cookie
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from transport_app import model, database
from transport_app.crud import crud_user
from transport_app.schemas import schemas_user, schemas_token
from fastapi.templating import Jinja2Templates

template = Jinja2Templates(directory="transport_app/template")


SECRET_KEY = "8dc23b8d0f3463589532b06f50c36056e5bbf29aeb6ae9bbb8646fcf0bc199e0"
ALGORITHM = "HS256"

model.Base.metadata.create_all(bind=database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(db: Session, email: str, password: str):
    user_data = crud_user.get_user_by_email(db, email)
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


async def get_current_user(access_token: str = Cookie(), db: Session = Depends(get_db)):
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
    user_data = crud_user.get_user_by_email(db, email=token_data.username)
    if user_data is None:
        raise credentials_exception
    return user_data


async def get_current_active_user(current_user: Annotated[schemas_user.User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def check_manager(user: schemas_user.UserCreate = Depends(get_current_active_user)):
    if user.user_type != 'manager':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions.")
    return user


async def check_accountant(user: schemas_user.UserCreate = Depends(get_current_active_user)):
    if user.user_type != 'accountant':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have the necessary permissions.")
    return user

