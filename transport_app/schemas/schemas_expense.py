import datetime

from pydantic import BaseModel
import datetime


class ExpenseBase(BaseModel):
    date: datetime.date | None
    description: str | None
    amount: int | None


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    driver_id: int
    driver_name: str

    class ConfigDict:
        from_attributes = True
