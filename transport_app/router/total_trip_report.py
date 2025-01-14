from fastapi import APIRouter, Depends, Request
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_trip
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/total-trip-report")
async def total_trip_report(request: Request, db: Session = Depends(get_db)):

    trips = crud_trip.get_trips(db)

    return template.TemplateResponse("total-trip-report.html", {"request": request, "trips": trips})
