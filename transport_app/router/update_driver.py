from fastapi import APIRouter, Depends, Request, Form
from starlette.responses import RedirectResponse
from transport_app.user_authentication import check_manager, get_db, template
from transport_app.crud import crud_driver
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/trucks", response_class=HTMLResponse)
async def truck_update_page(
        request: Request,
        db: Session = Depends(get_db)
):
    db_driver = crud_driver.get_drivers(db)
    return template.TemplateResponse("trucks.html", {"request": request, "drivers": db_driver})


@router.post("/driver-update/{driver_id}", response_class=HTMLResponse)
async def update_truck(
        driver_id: int,
        first_name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
        phone_number: str | None = Form(default=None),
        plate_number: str | None = Form(default=None),
        db: Session = Depends(get_db),
):
    if plate_number:
        plate_number = plate_number.replace(' ','').upper()
    if first_name:
        first_name = first_name.replace(' ','').upper()
    if last_name:
        last_name = last_name.replace(' ','').upper()

    driver_details = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "plate_number": plate_number
    }
    db_driver = crud_driver.update_driver(db, driver_id, driver_details)

    return RedirectResponse(url="/trucks", status_code=303)

