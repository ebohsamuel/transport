from datetime import datetime
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
        select(model.Expense).limit(1500)
        .options(selectinload(model.Expense.truck))
        .order_by(desc(model.Expense.date))
    )
    return result.all()


async def get_expenses_between_date(db: AsyncSession, start_date: str, end_date: str):
    start = datetime.strptime(start_date, "%Y-%m-%d").date()
    end = datetime.strptime(end_date, "%Y-%m-%d").date()

    result = await db.scalars(
        select(model.Expense)
        .options(selectinload(model.Expense.truck))
        .filter(model.Expense.date.between(start, end))
        .order_by(desc(model.Expense.date))
    )
    return result.all()


async def get_yearly_expenses_by_truck(db: AsyncSession, year: str | None, truck: str | None):
    start_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d").date()
    end_date = datetime.strptime(f"{year}-12-31", "%Y-%m-%d").date()

    stmt = (
        select(model.Expense)
        .join(model.Expense.truck)  # join to Driver table via relationship
        .filter(
            model.Expense.date.between(start_date, end_date)
        )
    )

    if truck:
        stmt = stmt.filter(model.Truck.plate_number == truck)

    result = await db.scalars(stmt)

    return result.all()


async def create_expense(db: AsyncSession, expense: schemas_expense.ExpenseCreate):
    db_expense = model.Expense(**expense.model_dump(exclude_none=True))
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
        if expense_details.get("date"):
            db_expense.date = expense_details.get("date")
        if expense_details.get("driver_name"):
            db_expense.driver_name = expense_details.get("driver_name")
        if expense_details.get("description"):
            db_expense.description = expense_details.get("description")
        if expense_details.get("amount"):
            db_expense.amount = expense_details.get("amount")
        if expense_details.get("truck_id"):
            db_expense.truck_id = expense_details.get("truck_id")
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
