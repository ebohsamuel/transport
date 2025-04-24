from pydantic import BaseModel


class UserBase(BaseModel):
    email: str | None = None
    full_name: str | None = None
    phone: str | None = None
    address: str | None = None
    next_of_kin: str | None = None
    next_of_kin_address: str | None = None
    next_of_kin_phone: str | None = None
    status: str | None = None
    role: str | None = None
    password: str | None = None


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int

    class ConfigDict:
        from_attributes = True
