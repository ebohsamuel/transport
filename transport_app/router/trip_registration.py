from fastapi import APIRouter, Depends, Request, HTTPException
from transport_app.user_authentication import check_manager, get_db,template
from transport_app.schemas import schemas_trip
from transport_app.crud import crud_trip, crud_driver
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/trip-registration-form/{driver_id}", response_class=HTMLResponse)
async def trip_registration_form(
        driver_id: int,
        request: Request,
        db: Session = Depends(get_db)
):
    db_driver = crud_driver.get_driver_by_id(db, driver_id)
    full_name = db_driver.first_name + ' ' + db_driver.last_name
    return template.TemplateResponse(
        'trip-registration-form.html', {'request': request, 'fullname': full_name, 'driver_id': driver_id}
    )


@router.post("/trip-registration")
async def register_new_trip(request: Request, db: Session = Depends(get_db)):

    data = await request.json()
    print(data)
    driver_id = data.pop('driver_id')
    trip = schemas_trip.TripCreate(**data)

    # check if the data contain atc number in other to perform some operation on it
    if trip.atc_order_number:
        # removing any space in the act number if it is given
        trip.atc_order_number = trip.atc_order_number.replace(' ','')
        atc_order_number = trip.atc_order_number

        # checking if a trip with the act number already exist, and if so stop the process
        db_trip = crud_trip.get_trip_by_atc(db=db, atc_order_number=atc_order_number)
        if db_trip:
            raise HTTPException(status_code=400, detail="The trip with the ATC order number already exists")

    # getting the driver full name
    db_driver = crud_driver.get_driver_by_id(db, driver_id)
    full_name = db_driver.first_name + ' ' + db_driver.last_name

    # creating a trip entry in the database
    db_trip = crud_trip.create_trip(db=db, trip=trip, driver_id=driver_id, driver_name=full_name)
    return {'detail': 'successful!', 'data': data}
