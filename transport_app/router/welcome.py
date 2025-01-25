from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.user_authentication import template, get_db, check_manager
from transport_app.crud import crud_driver


router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/welcome", response_class=HTMLResponse)
async def welcome_page(request: Request, db:AsyncSession = Depends(get_db)):
    drivers = await crud_driver.get_drivers(db)
    return template.TemplateResponse("welcome.html", {"request": request, "drivers": drivers})
