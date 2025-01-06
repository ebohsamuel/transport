from pydantic import BaseModel
import datetime


class TripBase(BaseModel):
    date: datetime.date | None
    atc_order_number: str | None
    dispatch: int | None
    bonus: int | None
    diesel_litres: float | None
    diesel_amount: int | None
    diesel_date: datetime.date | None
    customer_name: str | None
    amount: float | None


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int
    driver_id: int
    driver_name: str

    class ConfigDict:
        from_attributes = True