from pydantic import BaseModel


class DriverBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    plate_number: str


class DriverCreate(DriverBase):
    pass


class Driver(DriverBase):
    id: int

    class ConfigDict:
        from_attributes = True
