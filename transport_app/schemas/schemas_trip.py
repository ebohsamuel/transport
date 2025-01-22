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


class TripCreate(TripBase):
    pass


class Trip(TripBase):
    id: int
    driver_id: int
    driver_name: str

    class ConfigDict:
        from_attributes = True