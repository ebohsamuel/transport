from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

from transport_app import model
from transport_app.schemas import schemas_truck


async def get_truck_by_id(truck_id: int, db: AsyncSession):
    result = await db.scalars(
        select(model.Truck)
        .options(
            selectinload(model.Truck.trip),
            selectinload(model.Truck.expense)
        )
        .filter(model.Truck.id == truck_id)
    )
    return result.first()


async def get_truck_by_plate_number(db: AsyncSession, plate_number: str):
    result = await db.scalars(select(model.Truck).filter(model.Truck.plate_number == plate_number))
    return result.first()


async def get_all_plate_numbers(db: AsyncSession):
    result = await db.scalars(
        select(model.Truck.plate_number)
        .where(model.Truck.driver_name.isnot(None))
    )
    return result.all()


async def get_trucks(db: AsyncSession):
    result = await db.scalars(select(model.Truck).order_by(desc(model.Truck.plate_number)))
    return result.all()


async def create_truck(db: AsyncSession, truck: schemas_truck.TruckCreate):
    db_driver = model.Truck(**truck.model_dump(exclude_none=True))
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


async def update_truck(db: AsyncSession, truck_id: int, truck_details: dict):
    try:
        db_driver = await get_truck_by_id(truck_id, db)
        if truck_details.get("driver_name"):
            db_driver.driver_name = truck_details.get("driver_name")
        if truck_details.get("address"):
            db_driver.address = truck_details.get("address")
        if truck_details.get("phone_number"):
            db_driver.phone_number = truck_details.get("phone_number")
        if truck_details.get("plate_number"):
            db_driver.plate_number = truck_details.get("plate_number")
        if truck_details.get("guarantor"):
            db_driver.guarantor = truck_details.get("guarantor")
        if truck_details.get("guarantor_phone"):
            db_driver.guarantor_phone = truck_details.get("guarantor_phone")
        if truck_details.get("guarantor_address"):
            db_driver.guarantor_address = truck_details.get("guarantor_address")
        if truck_details.get("vehicle_model"):
            db_driver.vehicle_model = truck_details.get("vehicle_model")
        if truck_details.get("tonnage"):
            db_driver.tonnage = truck_details.get("tonnage")

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
