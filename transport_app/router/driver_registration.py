from transport_app.user_authentication import check_manager, get_db
from fastapi.responses import RedirectResponse
from fastapi import APIRouter, Form, Depends
from transport_app.crud import crud_driver
from sqlalchemy.orm import Session
from transport_app.schemas import schemas_driver


router = APIRouter(dependencies=[Depends(check_manager)])


@router.post("/driver-registration")
async def create_driver_details(
        first_name: str = Form(),
        last_name: str = Form(),
        phone_number: str = Form(),
        plate_number: str = Form(),
        db: Session = Depends(get_db),
):
    plate_number = plate_number.replace(" ","").upper()
    last_name = last_name.replace(" ","").upper()
    first_name = first_name.replace(" ","").upper()
    db_driver = crud_driver.get_driver_by_plate_number(db, plate_number)
    if db_driver:
        return {'message': 'truck already registered'}
    driver = schemas_driver.DriverCreate(
        first_name=first_name,
        last_name=last_name,
        phone_number=phone_number,
        plate_number=plate_number
    )

    db_driver = crud_driver.create_driver(db, driver)
    return RedirectResponse(url="/welcome", status_code=303)
