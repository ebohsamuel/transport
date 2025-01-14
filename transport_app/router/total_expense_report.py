from fastapi import APIRouter, Depends, Request
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.crud import crud_expense
from sqlalchemy.orm import Session


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/total-expense-report")
async def total_expense_report(request: Request, db: Session = Depends(get_db)):

    expenses = crud_expense.get_expenses(db)

    return template.TemplateResponse("total-expense-report.html", {"request": request, "expenses": expenses})
