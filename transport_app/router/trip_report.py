from fastapi import APIRouter, Depends, Request
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_driver
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/trip-report/{plate_number}/{driver_id}")
async def trip_report(
        plate_number: str,
        driver_id: int,
        request: Request,
        db: Session = Depends(get_db),
):

    driver = crud_driver.get_driver_by_id(db, driver_id)
    driver_trips = driver.trip
    return template.TemplateResponse(
        "trip-report.html",
        {
            "request": request,
            "driver_trips": driver_trips,
            "plate_number": plate_number,
            "driver_id": driver_id
        }
    )
