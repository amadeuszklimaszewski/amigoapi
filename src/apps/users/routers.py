from uuid import UUID
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from src.apps.users.models import User

from src.apps.users.schemas import UserLoginSchema, UserOutputSchema, UserRegisterSchema
from src.apps.users.services import UserService
from src.apps.jwt.schemas import TokenSchema
from src.database.connection import get_db
from src.dependencies.users import authenticate_user

user_router = APIRouter(prefix="/users")


# @user_router.get("/")
# def root():
#     return {"Users": "users"}


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


@user_router.get(
    "/",
    tags=["users"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutputSchema],
)
def get_users(db: Session = Depends(get_db)) -> list[UserOutputSchema]:
    return [UserOutputSchema.from_orm(user) for user in db.query(User).all()]


@user_router.get(
    "/profile",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
def get_logged_user(
    request_user: User = Depends(authenticate_user),
) -> UserOutputSchema:
    return UserOutputSchema.from_orm(request_user)


@user_router.get(
    "/{user_id}",
    tags=["users"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
def get_user(user_id: UUID, db: Session = Depends(get_db)) -> UserOutputSchema:
    return UserOutputSchema.from_orm(db.query(User).filter_by(id=user_id).first())
