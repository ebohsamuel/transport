from pydantic import BaseModel
from datetime import date


class TripBase(BaseModel):
    loading_date: date | None
    atc_order_number: str | None
    dispatch: int | None
    bonus: int | None
    diesel_litres: int | None
    diesel_amount: int | None
    diesel_date: date | None
    customer_name: str | None
    amount: int | None
    truck_id: int | None
    driver_name: str | None


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int

    class ConfigDict:
        from_attributes = True
