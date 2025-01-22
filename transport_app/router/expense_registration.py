from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import check_manager, get_db, template
from transport_app.schemas import schemas_expense
from transport_app.crud import crud_expense, crud_driver
from fastapi.responses import HTMLResponse


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/expense-registration-form/{driver_id}", response_class=HTMLResponse)
async def expense_registration_form(
        driver_id: int,
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    db_driver = await crud_driver.get_driver_by_id(driver_id, db)
    full_name = db_driver.first_name + ' ' + db_driver.last_name
    return template.TemplateResponse(
        'expense-registration-form.html', {'request': request, 'fullname': full_name, 'driver_id': driver_id}
    )


@router.post("/expense-registration")
async def register_new_trip(request: Request, db: AsyncSession = Depends(get_db)):

    data = await request.json()
    print(data)
    driver_id = data.pop('driver_id')
    driver_name = data.pop('driver_name')
    expense = schemas_expense.ExpenseCreate(**data)

    # creating a expense entry in the database
    db_trip = await crud_expense.create_expense(db, expense, driver_id, driver_name)
    return {'detail': 'successful!', 'data': data}
