from pydantic import BaseModel


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str
    user_type: str


class User(UserBase):
    id: int
    is_active: bool

    class ConfigDict:
        from_attributes = True
