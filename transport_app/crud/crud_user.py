import os
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from transport_app import model
from transport_app.schemas import schemas_user


scheme = os.getenv("scheme")

pwd_context = CryptContext(schemes=[scheme], deprecated="auto")


async def create_user(db: AsyncSession, user: schemas_user.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = model.User(email=user.email, hashed_password=hashed_password, user_type=user.user_type)
    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise


async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.scalars(select(model.User).filter(model.User.email == email))
    return result.first()


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.scalars(select(model.User).filter(model.User.id == user_id))
    return result.first()


async def get_users(db: AsyncSession):
    result = await db.scalars(select(model.User))
    return result.all()


async def update_user(db: AsyncSession, user_details: dict, user_id: int):
    db_user = await get_user_by_id(db, user_id)
    try:
        if user_details["is_active"]:
            db_user.is_active = user_details["is_active"]
        if user_details["user_type"]:
            db_user.user_type = user_details["user_type"]
        if user_details["email"]:
            db_user.email = user_details["email"]
        if user_details["password"]:
            db_user.hashed_password = pwd_context.hash(user_details["password"])
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise
