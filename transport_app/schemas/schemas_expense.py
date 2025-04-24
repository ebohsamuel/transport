from pydantic import BaseModel
import datetime


class ExpenseBase(BaseModel):
    date: datetime.date | None
    description: str | None
    amount: int | None
    truck_id: int | None
    driver_name: str | None


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int

    class ConfigDict:
        from_attributes = True
