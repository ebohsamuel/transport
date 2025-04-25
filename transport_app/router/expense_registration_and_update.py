from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from transport_app.user_authentication import get_current_active_user, get_db, template
from transport_app.schemas import schemas_expense, schemas_user
from transport_app.crud import crud_expense


router = APIRouter(dependencies=[Depends(get_current_active_user)])


@router.get("/expenses")
async def expense_(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: schemas_user.User = Depends(get_current_active_user)
):
    expenses = await crud_expense.get_expenses(db)
    return template.TemplateResponse(
        "expenses.html",
        {
            "request": request,
            "expenses": expenses,
            "full_name": user.full_name
        }
    )


@router.post("/expense-registration")
async def create_new_expense(expense: schemas_expense.ExpenseCreate, db: AsyncSession = Depends(get_db)):

    # creating a expense entry in the database
    db_expense = await crud_expense.create_expense(db, expense)
    return {'detail': 'successful!'}


@router.post("/expense-update")
async def updated_expense(
        expense: schemas_expense.Expense,
        db: AsyncSession = Depends(get_db),
):
    expense_details = expense.model_dump(exclude_none=True)
    expense_id = expense_details.pop("id")
    db_expense = await crud_expense.update_expense(db, expense_id, expense_details)
    return {'detail': 'successful!'}
