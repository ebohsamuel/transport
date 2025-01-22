from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import desc, select
from sqlalchemy.orm import selectinload

from transport_app import model
from transport_app.schemas import schemas_expense


async def get_expense_by_id(db: AsyncSession, expense_id: int):
    result = await db.scalars(select(model.Expense).filter(model.Expense.id == expense_id))
    return result.first()


async def get_expenses(db: AsyncSession):
    result = await db.scalars(
        select(model.Expense)
        .options(selectinload(model.Expense.driver))
        .order_by(desc(model.Expense.date))
    )
    return result.all()


async def create_expense(db: AsyncSession, expense: schemas_expense.ExpenseCreate, driver_id: int, driver_name: str):
    db_expense = model.Expense(**expense.model_dump(exclude_none=True), driver_id=driver_id, driver_name=driver_name)
    try:
        db.add(db_expense)
        await db.commit()
        await db.refresh(db_expense)
        return db_expense
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise


async def update_expense(db: AsyncSession, expense_id: int, expense_details: dict):
    db_expense = await get_expense_by_id(db, expense_id)
    try:
        if expense_details["date"]:
            db_expense.date = expense_details["date"]
        if expense_details["driver_name"]:
            db_expense.driver_name = expense_details["driver_name"]
        if expense_details["description"]:
            db_expense.description = expense_details["description"]
        if expense_details["amount"]:
            db_expense.amount = expense_details["amount"]
        await db.commit()
        await db.refresh(db_expense)
        return db_expense
    except SQLAlchemyError as e:
        await db.rollback()
        print(f"An error occurred: {e}")
        raise
    except ValueError as e:
        await db.rollback()
        raise
