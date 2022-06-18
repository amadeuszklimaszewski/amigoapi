from uuid import UUID
from fastapi import Depends, status
from fastapi.routing import APIRouter
from fastapi_jwt_auth import AuthJWT

from sqlalchemy.orm import Session
from src.apps.users.models import User

from src.apps.users.schemas import (
    UserLoginSchema,
    UserOutputSchema,
    UserRegisterSchema,
    UserUpdateSchema,
)
from src.apps.users.services import UserService
from src.apps.jwt.schemas import TokenSchema
from src.database.connection import get_db
from src.dependencies.users import authenticate_user

user_router = APIRouter(prefix="/users")


@user_router.post(
    "/register/",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutputSchema,
)
def register_user(
    user_register_schema: UserRegisterSchema,
    user_service: UserService = Depends(),
    session: Session = Depends(get_db),
) -> UserOutputSchema:
    user = user_service.register_user(user_register_schema, session=session)
    return UserOutputSchema.from_orm(user)


@user_router.post(
    "/login/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=TokenSchema,
)
def login_user(
    user_login_schema: UserLoginSchema,
    auth_jwt: AuthJWT = Depends(),
    user_service: UserService = Depends(),
    session: Session = Depends(get_db),
) -> TokenSchema:
    user = user_service.authenticate(**user_login_schema.dict(), session=session)
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
def get_users(
    user_service: UserService = Depends(),
    session: Session = Depends(get_db),
) -> list[UserOutputSchema]:
    return [
        UserOutputSchema.from_orm(user)
        for user in user_service.get_user_list(session=session)
    ]


@user_router.get(
    "/profile/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
def get_logged_user(
    request_user: User = Depends(authenticate_user),
) -> UserOutputSchema:
    return UserOutputSchema.from_orm(request_user)


@user_router.get(
    "/{user_id}/",
    tags=["users"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
def get_user(
    user_id: UUID,
    user_service: UserService = Depends(),
    session: Session = Depends(get_db),
) -> UserOutputSchema:
    user = user_service.get_user_by_id(user_id=user_id, session=session)
    return UserOutputSchema.from_orm(user)


@user_router.put(
    "/profile/",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    response_model=UserOutputSchema,
)
def update_user(
    update_schema: UserUpdateSchema,
    user: User = Depends(authenticate_user),
    service: UserService = Depends(),
    session: Session = Depends(get_db),
) -> UserOutputSchema:
    updated_user = service.update_user(user=user, schema=update_schema, session=session)
    return UserOutputSchema.from_orm(updated_user)
