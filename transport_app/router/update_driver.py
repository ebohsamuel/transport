from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from transport_app.user_authentication import check_manager, get_db, template
from transport_app.crud import crud_driver
from fastapi.responses import HTMLResponse


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/trucks", response_class=HTMLResponse)
async def truck_update_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    db_driver = await crud_driver.get_drivers(db)
    return template.TemplateResponse("trucks.html", {"request": request, "drivers": db_driver})


@router.post("/driver-update/{driver_id}", response_class=HTMLResponse)
async def update_truck(
        driver_id: int,
        first_name: str | None = Form(default=None),
        last_name: str | None = Form(default=None),
        phone_number: str | None = Form(default=None),
        plate_number: str | None = Form(default=None),
        db: AsyncSession = Depends(get_db),
):
    if plate_number:
        plate_number = plate_number.replace(' ','').lower()
    if first_name:
        first_name = first_name.replace(' ','').lower()
    if last_name:
        last_name = last_name.replace(' ','').lower()

    driver_details = {
        "first_name": first_name,
        "last_name": last_name,
        "phone_number": phone_number,
        "plate_number": plate_number
    }
    db_driver = await crud_driver.update_driver(db, driver_id, driver_details)

    return RedirectResponse(url="/trucks", status_code=303)

