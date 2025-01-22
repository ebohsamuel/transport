from fastapi import FastAPI, Request
from contextlib import AsyncExitStack

from transport_app.crud import crud_user
from transport_app.schemas import schemas_user
from transport_app.database import async_engine, Base
from transport_app.user_authentication import template, get_db
from transport_app.router import login, welcome, user_registration, logout, update_user, driver_registration
from transport_app.router import trip_registration, trip_update, expense_registration, update_expense
from transport_app.router import update_driver, trip_report, expense_report, total_trip_report, total_expense_report
from transport_app.router import notification


app = FastAPI()

app.include_router(notification.router)
app.include_router(login.router)
app.include_router(logout.router)
app.include_router(welcome.router)
app.include_router(user_registration.router)
app.include_router(update_user.router)
app.include_router(driver_registration.router)
app.include_router(trip_registration.router)
app.include_router(trip_update.router)
app.include_router(expense_registration.router)
app.include_router(update_expense.router)
app.include_router(update_driver.router)
app.include_router(trip_report.router)
app.include_router(expense_report.router)
app.include_router(total_trip_report.router)
app.include_router(total_expense_report.router)


@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db_generator = get_db()
    db = await anext(db_generator)
    try:
        data = {
            "email": "eng1102493@gmail.com",
            "password": "24bennSOO",
            "user_type": "manager"
        }
        schema_data = schemas_user.UserCreate(**data)

        db_user = await crud_user.get_user_by_email(db, email=schema_data.email)
        if not db_user:
            user = await crud_user.create_user(db=db, user=schema_data)
            print("Admin user created.")
        else:
            print("Admin user already exists.")
    finally:
        await db_generator.aclose()


@app.get("/")
async def read_index(request: Request):
    return template.TemplateResponse("login.html", {"request": request})
