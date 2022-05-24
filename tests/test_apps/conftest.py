import pytest
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.apps.users.models import User
from src.apps.users.schemas import UserOutputSchema, UserRegisterSchema
from src.apps.users.services import UserService
from src.apps.recipes.schemas import RecipeInputSchema, RecipeOutputSchema
from src.apps.recipes.services import RecipeService


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
def recipe_data() -> dict[str, str | int]:
    return {
        "title": "test",
        "time_required": "2 hours",
        "servings": 4,
        "description": "test description",
    }


@pytest.fixture
def recipe_in_db(
    recipe_data: dict[str, str | int], register_user: UserOutputSchema, session: Session
) -> RecipeOutputSchema:
    user = session.query(User).filter_by(id=register_user.id).first()
    schema = RecipeInputSchema(**recipe_data)
    return RecipeService.create_recipe(schema=schema, user=user, db=session)