from fastapi import Depends, responses, status
from fastapi.routing import APIRouter
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session

from src.apps.users.schemas import UserLoginSchema, UserOutputSchema, UserRegisterSchema
from src.apps.users.services import UserService
from src.apps.users.jwt_schemas import TokenSchema
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


@user_router.post(
    "/login", tags=["users"], status_code=status.HTTP_200_OK, response_model=TokenSchema
)
def login_user(
    user_login_schema: UserLoginSchema,
    auth_jwt: AuthJWT = Depends(),
    user_service: UserService = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate(**user_login_schema.dict(), db=db)
    user_schema = UserOutputSchema.from_orm(user)
    access_token = auth_jwt.create_access_token(subject=user_schema.json())

    return TokenSchema(access_token=access_token)


def get_user():
    return


def update_user():
    return
