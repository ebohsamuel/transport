from sqlalchemy.ext.asyncio import AsyncSession

from transport_app.schemas import schemas_user
from transport_app.crud import crud_user
from fastapi import Depends, APIRouter, Request, HTTPException
from transport_app.user_authentication import get_db, check_manager, template, get_current_active_user

router = APIRouter(dependencies=[Depends(check_manager)])


@router.get("/users")
async def user_list(
        request: Request,
        db: AsyncSession = Depends(get_db),
        user: schemas_user.User = Depends(get_current_active_user)
):
    users = await crud_user.get_users(db)
    return template.TemplateResponse(
        "user-list.html",
        {
            "request": request,
            "users": users,
            "full_name": user.full_name
        }
    )


@router.post("/user-registration")
async def enter_new_user(
        user: schemas_user.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    check_user = await crud_user.get_user_by_email(db, user.email)
    if check_user:
        raise HTTPException(status_code=400, detail="user already exist")

    db_user = await crud_user.create_user(db, user)
    return {'message': 'successful!'}


@router.post(path="/user-update")
async  def update_user(
        user: schemas_user.User,
        db: AsyncSession = Depends(get_db),

):
    if user.email:
        check_user = await crud_user.get_user_by_email(db, user.email)
        if check_user:
            raise HTTPException(status_code=400, detail="user already exist")

    user_details = user.model_dump(exclude_none=True)
    user_id = user_details.pop("id")

    db_user = await crud_user.update_user(db, user_details=user_details, user_id=user_id)
    return {'message': 'successful!'}
