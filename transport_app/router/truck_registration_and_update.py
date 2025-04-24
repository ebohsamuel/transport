from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import get_current_active_user, get_db, template
from fastapi import APIRouter, Depends, Request, HTTPException
from transport_app.crud import crud_truck
from transport_app.schemas import schemas_truck


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/truck-list")
async def truck_list(request: Request, db: AsyncSession = Depends(get_db)):
    trucks = await crud_truck.get_trucks(db)
    return template.TemplateResponse("truck-list.html", {"request": request, "trucks": trucks})


@router.post("/truck-registration")
async def create_truck(
        truck_details: schemas_truck.TruckCreate,
        db: AsyncSession = Depends(get_db)
):
    db_truck = await crud_truck.get_truck_by_plate_number(db, truck_details.plate_number)
    if db_truck:
        raise HTTPException(
            status_code=400,
            detail="truck already registered"
        )

    db_truck = await crud_truck.create_truck(db, truck=truck_details)
    return {'message': 'successful'}


@router.post("/truck-update")
async def update_truck(
        truck: schemas_truck.Truck,
        db: AsyncSession = Depends(get_db),
):

    if truck.plate_number:
        db_truck = await crud_truck.get_truck_by_plate_number(db, truck.plate_number)
        if db_truck:
            raise HTTPException(
                status_code=400,
                detail="truck already registered"
            )

    truck_details = truck.model_dump(exclude_none=True)
    truck_id = truck_details.pop("id")

    db_truck = await crud_truck.update_truck(db, truck_id, truck_details)

    return {'message': 'successful'}
