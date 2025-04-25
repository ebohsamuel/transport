import asyncio
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.schemas import schemas_user
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_trip


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/trip-report")
async def trip_report(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: schemas_user.User = Depends(get_current_active_user)
):
    trips = await crud_trip.get_trips(db)
    return template.TemplateResponse(
        "trip-report.html",
        {
            "request": request,
            "trips": trips,
            "full_name": user.full_name
        }
    )


@router.get("/trip-filter")
async def trip_filter(start_date: str, end_date: str, db: AsyncSession = Depends(get_db)):
    trips = await crud_trip.get_trip_between_date(db, start_date, end_date)
    data = []
    for trip in trips:
        trip_dict = trip.__dict__.copy()
        trip_dict["plate_number"] = trip.truck.plate_number
        data.append(trip_dict)
        await asyncio.sleep(0)
    return {"data": data}
