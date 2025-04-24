from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_expense


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/expense-report")
async def expense_report(request: Request, db: AsyncSession = Depends(get_db)):
    expenses = await crud_expense.get_expenses(db)
    return template.TemplateResponse("expense-report.html", {"request": request, "expenses": expenses})


@router.get("/expense-filter")
async def expense_filter(start_date: str, end_date: str, db: AsyncSession = Depends(get_db)):
    expenses = await crud_expense.get_expenses_between_date(db, start_date, end_date)
    return {"expenses": expenses}
