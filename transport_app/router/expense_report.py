import asyncio

from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.schemas import schemas_user
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_expense


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/expense-report")
async def expense_report(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: schemas_user.User = Depends(get_current_active_user)
):
    expenses = await crud_expense.get_expenses(db)
    return template.TemplateResponse(
        "expense-report.html",
        {
            "request": request,
            "expenses": expenses,
            "full_name": user.full_name
        }
    )


@router.get("/expense-filter")
async def expense_filter(start_date: str, end_date: str, db: AsyncSession = Depends(get_db)):
    expenses = await crud_expense.get_expenses_between_date(db, start_date, end_date)
    data = []
    for expense in expenses:
        expense_dict = expense.__dict__.copy()
        expense_dict["plate_number"] = expense.truck.plate_number
        data.append(expense_dict)
        await asyncio.sleep(0)
    return {"data": data}
