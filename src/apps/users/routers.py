from fastapi import Depends, status
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session

from src.apps.users.schemas import UserLoginSchema, UserOutputSchema, UserRegisterSchema
from src.apps.users.services import UserService

from src.database.connection import get_db

user_router = APIRouter(prefix="/users")


@user_router.get("/")
def root():
    return {"Users": "users"}


@user_router.post(
    "/register",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutputSchema,
)
def register_user(
    user_register_schema: UserRegisterSchema,
    user_service: UserService = Depends(),
    db: Session = Depends(get_db),
):
    user_schema = user_service.register_user(user_register_schema, db=db)
    return user_schema


@user_router.post("/login", tags=["users"])
def login_user(user_login_schema: UserLoginSchema):
    return


def get_user():
    return


def update_user():
    return
