from sqlalchemy.orm import Session
from passlib.context import CryptContext

from transport_app import model
from transport_app.schemas import schemas_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: schemas_user.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = model.User(email=user.email, hashed_password=hashed_password, user_type=user.user_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()


def get_users(db: Session):
    return db.query(model.User).all()


def update_user(db: Session, user_details: dict, user_id: int):
    db_user = get_user_by_id(db, user_id)
    if user_details["is_active"]:
        db_user.is_active = user_details["is_active"]
    if user_details["user_type"]:
        db_user.user_type = user_details["user_type"]
    if user_details["email"]:
        db_user.email = user_details["email"]
    if user_details["password"]:
        db_user.hashed_password = pwd_context.hash(user_details["password"])
    db.commit()
    db.refresh(db_user)
    return db_user
