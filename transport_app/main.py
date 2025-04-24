from fastapi import FastAPI, Request
import os
from transport_app.crud import crud_user
from transport_app.schemas import schemas_user
from transport_app.database import async_engine, Base
from transport_app.user_authentication import template, get_db
from transport_app.router import login, dashboard, user_registration_and_update, logout, truck_registration_and_update
from transport_app.router import trip_registration_and_update, expense_registration_and_update
from transport_app.router import trip_report, expense_report


app = FastAPI()

app.include_router(login.router)
app.include_router(logout.router)
app.include_router(dashboard.router)
app.include_router(user_registration_and_update.router)
app.include_router(truck_registration_and_update.router)
app.include_router(trip_registration_and_update.router)
app.include_router(expense_registration_and_update.router)
app.include_router(trip_report.router)
app.include_router(expense_report.router)

admin_email = "eng1102493@gmail.com"
admin_password = "24bennSOO"
role = "manager"
status = "active"


@app.on_event("startup")
async def on_startup():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    db_generator = get_db()
    db = await anext(db_generator)
    try:
        data = {
            "email": admin_email,
            "password": admin_password,
            "role": role,
            "status": status
        }
        schema_data = schemas_user.UserCreate(**data)

        db_user = await crud_user.get_user_by_email(db, email=schema_data.email)
        if not db_user:
            user = await crud_user.create_user(db=db, user=schema_data)
    finally:
        await db_generator.aclose()


@app.get("/")
async def read_index(request: Request):
    return template.TemplateResponse("login.html", {"request": request})
