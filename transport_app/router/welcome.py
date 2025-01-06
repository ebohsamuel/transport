from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

from transport_app.user_authentication import template, get_db
from transport_app.crud import crud_driver


router = APIRouter()


@router.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request, db:Session = Depends(get_db)):
    drivers = crud_driver.get_drivers(db)
    return template.TemplateResponse("welcome.html", {"request": request, "drivers": drivers})
