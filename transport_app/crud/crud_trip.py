from sqlalchemy.orm import Session
from sqlalchemy import between, desc

from transport_app import model
from transport_app.schemas import schemas_trip
from datetime import date


def get_trip_by_id(db: Session, trip_id: int):
    return db.query(model.Trip).filter(model.Trip.id == trip_id).first()


def get_trip_by_atc(db: Session, atc_order_number: str):
    return db.query(model.Trip).filter(model.Trip.atc_order_number == atc_order_number).first()



def get_trips(db: Session):
    return db.query(model.Trip).order_by(desc(model.Trip.date)).all()


def get_trips_between_dates(db: Session, start_date: date, end_date: date):
    return db.query(model.Trip).filter(
        between(model.Trip.date, start_date, end_date)).order_by(desc(model.Trip.date)).all()


def create_trip(db: Session, trip: schemas_trip.TripCreate, driver_id: int, driver_name: str):
    db_trip = model.Trip(**trip.model_dump(exclude_none=True), driver_id=driver_id, driver_name=driver_name)
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return db_trip


def update_trip(db: Session, trip_id: int, trip_details: dict):
    db_trip = get_trip_by_id(db, trip_id)
    if trip_details["date"]:
        db_trip.date = trip_details["date"]
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

    db.commit()
    db.refresh(db_trip)
    return db_trip


def get_driver_trips_between_dates(db: Session, driver_id: int, start_date: date, end_date: date):
    return db.query(model.Trip).filter(
        model.Trip.driver_id == driver_id,
        between(model.Trip.date, start_date, end_date)).order_by(desc(model.Trip.date)).all()

