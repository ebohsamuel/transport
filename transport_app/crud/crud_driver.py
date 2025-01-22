from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

from transport_app import model
from transport_app.schemas import schemas_driver


async def get_driver_by_id(driver_id: int, db: AsyncSession):
    result = await db.scalars(
        select(model.Driver)
        .options(
            selectinload(model.Driver.trip),
            selectinload(model.Driver.expense)
        )
        .filter(model.Driver.id == driver_id)
    )
    return result.first()


async def get_driver_by_plate_number(db: AsyncSession, plate_number: str):
    result = await db.scalars(select(model.Driver).filter(model.Driver.plate_number == plate_number))
    return result.first()


async def get_drivers(db: AsyncSession):
    result = await db.scalars(select(model.Driver).order_by(desc(model.Driver.plate_number)))
    return result.all()


async def create_driver(db: AsyncSession, driver: schemas_driver.DriverCreate):
    db_driver = model.Driver(**driver.model_dump())
    try:
        db.add(db_driver)
        await db.commit()
        await db.refresh(db_driver)
        return db_driver
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise


async def update_driver(db: AsyncSession, driver_id: int, driver_details: dict):
    try:
        db_driver = await get_driver_by_id(driver_id, db)
        if driver_details["first_name"]:
            db_driver.first_name = driver_details["first_name"]
        if driver_details["last_name"]:
            db_driver.last_name = driver_details["last_name"]
        if driver_details["phone_number"]:
            db_driver.phone_number = driver_details["phone_number"]
        if driver_details["plate_number"]:
            db_driver.plate_number = driver_details["plate_number"]

        await db.commit()
        await db.refresh(db_driver)
        return db_driver
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise
