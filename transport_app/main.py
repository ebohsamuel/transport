from fastapi import FastAPI, Request
from transport_app.user_authentication import template
from transport_app.router import login, welcome, user_registration, logout, update_user, driver_registration
from transport_app.router import trip_registration, trip_update, expense_registration, update_expense
from transport_app.router import update_driver, trip_report, expense_report

app = FastAPI()

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


@app.get("/")
async def read_index(request: Request):
    return template.TemplateResponse("login.html", {"request": request})
