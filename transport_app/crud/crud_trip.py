from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

from transport_app import model
from transport_app.schemas import schemas_trip


async def get_trip_by_id(db: AsyncSession, trip_id: int):
    result = await db.scalars(select(model.Trip).filter(model.Trip.id == trip_id))
    return result.first()


async def get_trip_by_atc(db: AsyncSession, atc_order_number: str):
    result = await db.scalars(select(model.Trip).filter(model.Trip.atc_order_number == atc_order_number))
    return result.first()


async def get_trips(db: AsyncSession):
    result = await db.scalars(
        select(model.Trip)
        .options(selectinload(model.Trip.driver)).
        order_by(desc(model.Trip.loading_date))
    )
    return result.all()


async def create_trip(db: AsyncSession, trip: schemas_trip.TripCreate, driver_id: int, driver_name: str):
    db_trip = model.Trip(**trip.model_dump(exclude_none=True), driver_id=driver_id, driver_name=driver_name)
    try:
        db.add(db_trip)
        await db.commit()
        await db.refresh(db_trip)
        return db_trip
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise


async def update_trip(db: AsyncSession, trip_id: int, trip_details: dict):
    db_trip = await get_trip_by_id(db, trip_id)
    try:
        if trip_details["loading_date"]:
            db_trip.loading_date = trip_details["loading_date"]
        if trip_details["atc_order_number"]:
            db_trip.atc_order_number = trip_details["atc_order_number"]
        if trip_details["customer_name"]:
            db_trip.customer_name = trip_details["customer_name"]
        if trip_details["amount"]:
            db_trip.amount = trip_details["amount"]
        if trip_details["dispatch"]:
            db_trip.dispatch = trip_details["dispatch"]
        if trip_details["bonus"]:
            db_trip.bonus = trip_details["bonus"]
        if trip_details["diesel_litres"]:
            db_trip.diesel_litres = trip_details["diesel_litres"]
        if trip_details["diesel_amount"]:
            db_trip.diesel_amount = trip_details["diesel_amount"]
        if trip_details["diesel_date"]:
            db_trip.diesel_date = trip_details["diesel_date"]
        if trip_details["driver_name"]:
            db_trip.driver_name = trip_details["driver_name"]

        await db.commit()
        await db.refresh(db_trip)
        return db_trip
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise
