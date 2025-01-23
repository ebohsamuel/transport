import asyncio
from fastapi import Request, APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from transport_app import model
from transport_app.user_authentication import template, get_db

router = APIRouter()


@router.get("/notification")
async def notification(request: Request):
    await asyncio.sleep(0)
    return template.TemplateResponse("notification.html", {"request": request})


@router.get("/notification-report")
async def report_notification(db: AsyncSession = Depends(get_db)):
    trip_result = await db.scalars(
        select(model.Trip)
        .options(selectinload(model.Trip.driver))
        .filter(model.Trip.customer_name.is_(None))
    )

    expense_result = await db.scalars(
        select(model.Expense)
        .options(selectinload(model.Expense.driver))
        .filter(model.Expense.amount.is_(None))
    )

    expenses = expense_result.all()
    trips = trip_result.all()
    trip_data = []
    expense_data = []

    for trip in trips:
        trip_data.append({
            'loading_date': trip.loading_date,
            'plate_number': trip.driver.plate_number
        })
        await asyncio.sleep(0)

    for expense in expenses:
        expense_data.append({
            'plate_number': expense.driver.plate_number,
            'expense_date': expense.date
        })
        await asyncio.sleep(0)

    return {"expenses": expense_data, "trips": trip_data}
