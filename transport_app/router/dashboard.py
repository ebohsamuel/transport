from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.schemas import schemas_user
from transport_app.user_authentication import template, get_db, get_current_active_user
from transport_app.crud import crud_truck, crud_expense, crud_trip

router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(
        request: Request,
        user: schemas_user.User = Depends(get_current_active_user)
):
    return template.TemplateResponse("dashboard.html", {"request": request, "full_name": user.full_name})


@router.get("/dashboard-report")
async def dashboard_report(
        year: str | None = None,
        truck: str | None = None,
        db: AsyncSession = Depends(get_db)
):
    expenses = await crud_expense.get_yearly_expenses_by_truck(db, year, truck)
    trips = await crud_trip.get_yearly_trips_by_truck(db, year, truck)
    return {"trips": trips, "expenses": expenses}


@router.get("/plate-number-list")
async def plate_number_list(db: AsyncSession = Depends(get_db)):
    plate_numbers = await crud_truck.get_all_plate_numbers(db)
    return {"plate_numbers": plate_numbers}


@router.get("/driver-name-and-truck-id")
async def plate_number_list(plate_number: str, db: AsyncSession = Depends(get_db)):
    truck = await crud_truck.get_truck_by_plate_number(db, plate_number)
    return {"truck_id": truck.id, "driver_name": truck.driver_name}
