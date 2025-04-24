from datetime import datetime

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
        select(model.Trip).limit(1500)
        .options(selectinload(model.Trip.truck)).
        order_by(desc(model.Trip.loading_date))
    )
    return result.all()


async def get_trip_between_date(db: AsyncSession, start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    result = await db.scalars(
        select(model.Trip)
        .options(selectinload(model.Trip.truck))
        .filter(model.Trip.loading_date.between(start, end))
        .order_by(desc(model.Trip.loading_date))
    )
    return result.all()


async def get_yearly_trips_by_truck(db: AsyncSession, year: str | None, truck: str | None):
    start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
    end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

    stmt = (
        select(model.Trip)
        .join(model.Trip.truck)  # join to Driver table via relationship
        .filter(
            model.Trip.loading_date.between(start_date, end_date)
        )
    )

    if truck:
        stmt = stmt.filter(model.Truck.plate_number == truck)

    result = await db.scalars(stmt)

    return result.all()


async def create_trip(db: AsyncSession, trip: schemas_trip.TripCreate):
    db_trip = model.Trip(**trip.model_dump(exclude_none=True))
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
        if trip_details.get("loading_date"):
            db_trip.loading_date = trip_details.get("loading_date")
        if trip_details.get("atc_order_number"):
            db_trip.atc_order_number = trip_details.get("atc_order_number")
        if trip_details.get("customer_name"):
            db_trip.customer_name = trip_details.get("customer_name")
        if trip_details.get("amount"):
            db_trip.amount = trip_details.get("amount")
        if trip_details.get("dispatch"):
            db_trip.dispatch = trip_details.get("dispatch")
        if trip_details.get("bonus"):
            db_trip.bonus = trip_details.get("bonus")
        if trip_details.get("diesel_litres"):
            db_trip.diesel_litres = trip_details.get("diesel_litres")
        if trip_details.get("diesel_amount"):
            db_trip.diesel_amount = trip_details.get("diesel_amount")
        if trip_details.get("diesel_date"):
            db_trip.diesel_date = trip_details.get("diesel_date")
        if trip_details.get("driver_name"):
            db_trip.driver_name = trip_details.get("driver_name")
        if trip_details.get("truck_id"):
            db_trip.truck_id = trip_details.get("truck_id")

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
