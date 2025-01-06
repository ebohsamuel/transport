import datetime
from fastapi import APIRouter, Depends, Request, Form
from transport_app.user_authentication import check_manager, get_db, template
from transport_app.crud import crud_trip
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/trips", response_class=HTMLResponse)
async def trip_update_page(
        request: Request,
        db: Session = Depends(get_db)
):

    trips = crud_trip.get_trips(db)
    return template.TemplateResponse("trips.html", {"request": request, "trips": trips})


@router.post("/trip-update/{trip_id}", response_class=HTMLResponse)
async def update_trip(
        trip_id: int,
        driver_name: str | None = Form(default=None),
        dispatch: int | None = Form(default=None),
        bonus: int | None = Form(default=None),
        date: datetime.date | None = Form(default=None),
        atc_order_number: str | None = Form(default=None),
        diesel_litres: float | None = Form(default=None),
        diesel_amount: int | None = Form(default=None),
        diesel_date: datetime.date | None = Form(default=None),
        customer_name: str | None = Form(default=None),
        amount: float | None = Form(default=None),
        db: Session = Depends(get_db),
):
    if driver_name:
        driver_name.upper()

    trip_details = {
        "date": date,
        "atc_order_number": atc_order_number,
        "customer_name": customer_name,
        "amount": amount,
        "dispatch": dispatch,
        "bonus": bonus,
        "diesel_litres": diesel_litres,
        "diesel_amount": diesel_amount,
        "diesel_date": diesel_date,
        "driver_name": driver_name
    }
    db_trip = crud_trip.update_trip(db, trip_id, trip_details)
    return RedirectResponse(url="/trips", status_code=303)
