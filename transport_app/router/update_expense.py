import datetime
from fastapi import APIRouter, Depends, Request, Form
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import RedirectResponse
from transport_app.user_authentication import check_manager, get_db, template
from transport_app.crud import crud_expense
from fastapi.responses import HTMLResponse


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/expenses", response_class=HTMLResponse)
async def expense_update_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    expenses = await crud_expense.get_expenses(db)
    return template.TemplateResponse("expenses.html", {"request": request, "expenses": expenses})


@router.post("/expense-update/{expense_id}", response_class=HTMLResponse)
async def updated_expense(
        expense_id: int,
        driver_name: str | None = Form(default=None),
        description: str | None = Form(default=None),
        date: datetime.date | None = Form(default=None),
        amount: int | None = Form(default=None),
        db: AsyncSession = Depends(get_db),
):
    if driver_name:
        driver_name.lower()

    expense_details = {
        "date": date,
        "description": description,
        "amount": amount,
        "driver_name": driver_name
    }
    db_expense = await crud_expense.update_expense(db, expense_id, expense_details)
    return RedirectResponse(url="/expenses", status_code=303)
