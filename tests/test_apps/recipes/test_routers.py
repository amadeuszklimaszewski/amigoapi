import pytest

from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.apps.recipes.schemas import RecipeOutputSchema
from src.apps.recipes.models import Recipe
from src.apps.users.schemas import UserOutputSchema


@pytest.fixture
def recipe_update_data() -> dict[str, str | int]:
    return {
        "title": "test update",
        "time_required": "3 hours",
        "servings": 6,
        "description": "test updated description",
    }


def test_get_recipe_list(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    session: Session,
):
    response: Response = client.get("/recipes/")
    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert len(response_body) == 1


def test_get_recipe_by_id(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    session: Session,
):
    response: Response = client.get(f"/recipes/{recipe_in_db.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == recipe_in_db.title
    assert response.json()["description"] == recipe_in_db.description


def test_authenticated_user_can_create_recipe(
    client: TestClient,
    recipe_data: dict[str, str | int],
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.post(
        "/recipes/", json=recipe_data, headers=user_bearer_token_header
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert len(session.query(Recipe).all()) == 1
    assert session.query(Recipe).first().user_id == register_user.id
    assert response.json()["title"] == recipe_data["title"]


def test_authenticated_user_can_update_recipe(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    recipe_update_data: dict[str, str | int],
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.put(
        f"/recipes/{recipe_in_db.id}/",
        json=recipe_update_data,
        headers=user_bearer_token_header,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(session.query(Recipe).all()) == 1
    assert session.query(Recipe).first().user_id == register_user.id
    assert response.json()["title"] == recipe_update_data["title"]
    assert response.json()["description"] == recipe_update_data["description"]


def test_other_user_cannot_update_recipe(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    recipe_update_data: dict[str, str | int],
    other_user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.put(
        f"/recipes/{recipe_in_db.id}/",
        json=recipe_update_data,
        headers=other_user_bearer_token_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "User is not owner of the recipe"
    assert (
        session.query(Recipe).filter_by(id=recipe_in_db.id).first().title
        == recipe_in_db.title
    )


def test_anonymous_user_cannot_update_recipe(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    recipe_update_data: dict[str, str | int],
    session: Session,
):
    response: Response = client.put(
        f"/recipes/{recipe_in_db.id}/", json=recipe_update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"
    assert (
        session.query(Recipe).filter_by(id=recipe_in_db.id).first().title
        == recipe_in_db.title
    )
