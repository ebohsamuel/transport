from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session
from transport_app import model
from transport_app.schemas.schemas_trip import Trip
from transport_app.user_authentication import template, get_db

router = APIRouter()


@router.get("/notification")
async def notification(request: Request):
    return template.TemplateResponse("notification.html", {"request": request})


@router.get("/notification-trip")
async def trip_notification(db: Session = Depends(get_db)):

    trips = db.query(model.Trip).filter(model.Trip.customer_name.is_(None))
    data = []
    for trip in trips:
        x = {
            'loading_date': trip.date,
            'plate_number': trip.driver.plate_number
        }
        data.append(x)
    return data


@router.get("/notification-expense")
async def expense_notification(db: Session = Depends(get_db)):
    expenses = db.query(model.Expense).filter(model.Expense.amount.is_(None))
    data = []
    for expense in expenses:
        data.append({
            'plate_number': expense.driver.plate_number,
            'expense_date': expense.date
        })
    return data
