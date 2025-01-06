from sqlalchemy.orm import Session
from sqlalchemy import desc

from transport_app import model
from transport_app.schemas import schemas_driver


def get_driver_by_id(db: Session, driver_id: int):
    return db.query(model.Driver).filter(model.Driver.id == driver_id).first()


def get_driver_by_plate_number(db: Session, plate_number: str):
    return db.query(model.Driver).filter(model.Driver.plate_number == plate_number).first()


def get_drivers(db: Session):
    return db.query(model.Driver).order_by(desc(model.Driver.plate_number)).all()


def create_driver(db: Session, driver: schemas_driver.DriverCreate):
    db_driver = model.Driver(**driver.model_dump())
    db.add(db_driver)
    db.commit()
    db.refresh(db_driver)
    return db_driver


def update_driver(db: Session, driver_id: int, driver_details: dict):
    db_driver = get_driver_by_id(db, driver_id)
    if driver_details["first_name"]:
        db_driver.first_name = driver_details["first_name"]
    if driver_details["last_name"]:
        db_driver.last_name = driver_details["last_name"]
    if driver_details["phone_number"]:
        db_driver.phone_number = driver_details["phone_number"]
    if driver_details["plate_number"]:
        db_driver.plate_number = driver_details["plate_number"]

    db.commit()
    db.refresh(db_driver)
    return db_driver
