from fastapi import APIRouter, Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.schemas import schemas_trip
from transport_app.crud import crud_trip


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/trips")
async def trip_(request: Request, db: AsyncSession = Depends(get_db)):
    trips = await crud_trip.get_trips(db)
    return template.TemplateResponse("trips.html", {"request": request, "trips": trips})


@router.post("/trip-registration")
async def create_new_trip(trip: schemas_trip.TripCreate, db: AsyncSession = Depends(get_db)):

    # check if the data contain atc number in other to perform some operation on it
    if trip.atc_order_number:
        # removing any space in the act number if it is given
        atc_order_number = trip.atc_order_number.replace(' ', '')

        # checking if a trip with the act number already exist, and if so stop the process
        db_trip = await crud_trip.get_trip_by_atc(db=db, atc_order_number=atc_order_number)
        if db_trip:
            raise HTTPException(
                status_code=400,
                detail=f"The trip with the ATC order number {atc_order_number} already exists"
            )

    # creating a trip entry in the database
    db_trip = await crud_trip.create_trip(db=db, trip=trip,)
    return {'detail': 'successful!'}


@router.post("/trip-update")
async def update_trip(
        trip: schemas_trip.Trip,
        db: AsyncSession = Depends(get_db),
):
    # check if the data contain atc number in other to perform some operation on it
    if trip.atc_order_number:
        # removing any space in the act number if it is given
        atc_order_number = trip.atc_order_number.replace(' ', '')

        # checking if a trip with the act number already exist, and if so stop the process
        db_trip = await crud_trip.get_trip_by_atc(db=db, atc_order_number=atc_order_number)
        if db_trip:
            raise HTTPException(
                status_code=400,
                detail=f"The trip with the ATC order number {atc_order_number} already exists"
            )

    trip_details = trip.model_dump(exclude_none=True)
    trip_id = trip_details.pop("id")

    db_trip = await crud_trip.update_trip(db, trip_id, trip_details)
    return {'detail': 'successful!'}
