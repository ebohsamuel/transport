import os
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from transport_app import model
from transport_app.schemas import schemas_user


scheme = "bcrypt"

pwd_context = CryptContext(schemes=(scheme), deprecated="auto")


async def create_user(db: AsyncSession, user: schemas_user.UserCreate):
    user_dict = user.model_dump(exclude_none=True)
    password = user_dict.pop("password")
    hashed_password = pwd_context.hash(password)
    db_user = model.User(**user_dict, hashed_password=hashed_password)
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
        if user_details.get("full_name"):
            db_user.full_name = user_details.get("full_name")
        if user_details.get("phone"):
            db_user.phone = user_details.get("phone")
        if user_details.get("email"):
            db_user.email = user_details.get("email")
        if user_details.get("password"):
            db_user.hashed_password = pwd_context.hash(user_details.get("password"))
        if user_details.get("address"):
            db_user.address = user_details.get("address")
        if user_details.get("next_of_kin"):
            db_user.next_of_kin = user_details.get("next_of_kin")
        if user_details.get("next_of_kin_address"):
            db_user.next_of_kin_address = user_details.get("next_of_kin_address")
        if user_details.get("next_of_kin_phone"):
            db_user.next_of_kin_phone = user_details.get("next_of_kin_phone")
        if user_details.get("status"):
            db_user.status = user_details.get("status")
        if user_details.get("role"):
            db_user.role = user_details.get("role")
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
