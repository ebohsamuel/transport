from pydantic import BaseModel


class TruckBase(BaseModel):
    driver_name: str | None
    vehicle_model: str | None
    tonnage: str | None
    phone_number: str | None
    plate_number: str | None
    address: str | None
    guarantor: str | None
    guarantor_phone: str | None
    guarantor_address: str | None


class TruckCreate(TruckBase):
    pass


class Truck(TruckBase):
    id: int

    class ConfigDict:
        from_attributes = True
