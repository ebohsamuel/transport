from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_expense


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/total-expense-report")
async def total_expense_report(request: Request, db: AsyncSession = Depends(get_db)):

    expenses = await crud_expense.get_expenses(db)

    return template.TemplateResponse("total-expense-report.html", {"request": request, "expenses": expenses})
