import pytest
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.apps.users.schemas import UserOutputSchema, UserRegisterSchema
from src.apps.users.services import UserService


@pytest.fixture
def user_register_data() -> dict[str, str]:
    return {
        "first_name": "name",
        "last_name": "name",
        "username": "username",
        "email": "testuser@google.com",
        "password": "test12345",
        "password2": "test12345",
        "birthday": "2000-01-01",
    }


@pytest.fixture
def register_user(
    user_register_data: dict[str, str], session: Session
) -> UserOutputSchema:
    schema = UserRegisterSchema(**user_register_data)
    return UserService.register_user(schema=schema, db=session)


@pytest.fixture
def user_bearer_token_header(register_user: UserOutputSchema) -> dict[str, str]:
    access_token = AuthJWT().create_access_token(subject=register_user.json())
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
def user_login_data(user_register_data: dict[str, str]) -> dict[str, str]:
    return {
        "email": user_register_data["email"],
        "password": user_register_data["password"],
    }
