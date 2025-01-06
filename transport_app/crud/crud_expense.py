from sqlalchemy.orm import Session
from sqlalchemy import between, desc

from transport_app import model
from transport_app.schemas import schemas_expense
from datetime import date


def get_expense_by_id(db: Session, expense_id: int):
    return db.query(model.Expense).filter(model.Expense.id == expense_id).first()


def get_driver_expense(db: Session, driver_id: int):
    return db.query(model.Expense).filter(
        model.Expense.driver_id == driver_id
    ).order_by(desc(model.Expense.date)).all()


def get_driver_expenses_between_dates(db: Session, driver_id: int, start_date: date, end_date: date):
    return db.query(model.Expense).filter(
        model.Expense.driver_id == driver_id,
        between(model.Expense.date, start_date, end_date)).order_by(desc(model.Expense.date)).all()


def get_expenses(db: Session):
    return db.query(model.Expense).order_by(desc(model.Expense.date)).all()


def get_expenses_between_dates(db: Session, start_date: date, end_date: date):
    return db.query(model.Expense).filter(
        between(model.Expense.date, start_date, end_date)).order_by(desc(model.Expense.date)).all()


def create_expense(db: Session, expense: schemas_expense.ExpenseCreate, driver_id: int, driver_name: str):
    db_expense = model.Expense(**expense.model_dump(exclude_none=True), driver_id=driver_id, driver_name=driver_name)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)
    return db_expense


def update_expense(db: Session, expense_id: int, expense_details: dict):
    db_expense = get_expense_by_id(db, expense_id)
    if expense_details["date"]:
        db_expense.date = expense_details["date"]
    if expense_details["driver_name"]:
        db_expense.driver_name = expense_details["driver_name"]
    if expense_details["description"]:
        db_expense.description = expense_details["description"]
    if expense_details["amount"]:
        db_expense.amount = expense_details["amount"]
    db.commit()
    db.refresh(db_expense)
    return db_expense
