from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_driver


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/expense-report/{plate_number}/{driver_id}")
async def expense_report(
        plate_number: str,
        driver_id: int,
        request: Request,
        db: AsyncSession = Depends(get_db),
):

    driver = await crud_driver.get_driver_by_id(driver_id, db)
    driver_expenses = driver.expense
    return template.TemplateResponse(
        "expense-report.html",
        {
            "request": request,
            "driver_expenses": driver_expenses,
            "plate_number": plate_number,
            "driver_id": driver_id
        }
    )
