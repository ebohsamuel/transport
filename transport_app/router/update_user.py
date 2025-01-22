from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.user_authentication import template, get_db, check_manager
from transport_app.crud import crud_user

router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/staff-list", response_class=HTMLResponse)
async def user_list(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    users = await crud_user.get_users(db)
    return template.TemplateResponse("user_list.html", {"request": request, "users": users})


@router.post(path="/user/update/{user_id}", response_class=RedirectResponse)
async  def update_user(
        user_id: int,
        is_active: bool | None = Form(default=None),
        user_type: str | None = Form(default=None),
        password: str | None = Form(default=None),
        email: str | None = Form(default=None),
        db: AsyncSession = Depends(get_db),

):
    user_details = {
        "is_active": is_active,
        "user_type": user_type,
        "password": password,
        "email": email,
    }
    db_user = await crud_user.update_user(db, user_details=user_details, user_id=user_id)
    return RedirectResponse(url="/staff-list", status_code=303)
