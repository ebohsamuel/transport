from transport_app.schemas import schemas_user
from transport_app.crud import crud_user
from fastapi import Depends, APIRouter
from transport_app.user_authentication import get_db, check_manager
from sqlalchemy.orm import Session

router = APIRouter(dependencies=[Depends(check_manager)])


@router.post("/staff-registration")
async def enter_new_user(
        data: schemas_user.UserCreate,
        db: Session = Depends(get_db)
):

    db_user = crud_user.create_user(db, data)
    return {'message': 'successful!', 'data': data}
