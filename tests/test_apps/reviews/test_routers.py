import pytest

from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.apps.reviews.models import Review
from src.apps.reviews.schemas import ReviewInputSchema, ReviewOutputSchema

from src.apps.reviews.services import ReviewService
from src.apps.recipes.schemas import RecipeOutputSchema
from src.apps.recipes.models import Recipe
from src.apps.users.models import User
from src.apps.users.schemas import UserOutputSchema


@pytest.fixture
def review_data() -> dict[str, str | int]:
    return {
        "title": "test",
        "rating": 5,
        "details": "test details",
    }


@pytest.fixture
def review_update_data() -> dict[str, str | int]:
    return {
        "title": "update",
        "rating": 4,
        "details": "test update",
    }


@pytest.fixture
def review_in_db(
    review_data: dict[str, str | int],
    recipe_in_db: RecipeOutputSchema,
    register_user: UserOutputSchema,
    session: Session,
) -> ReviewOutputSchema:
    user = session.query(User).filter_by(id=register_user.id).first()
    schema = ReviewInputSchema(**review_data)
    return ReviewService.create_review(
        schema=schema, recipe_id=recipe_in_db.id, user=user, session=session
    )


def test_get_review_list(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    review_in_db: ReviewOutputSchema,
    session: Session,
):
    response: Response = client.get(f"/reviews/{recipe_in_db.id}/")
    assert response.status_code == status.HTTP_200_OK
    response_body = response.json()
    assert len(response_body) == 1


def test_get_review_by_id(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    review_in_db: ReviewOutputSchema,
    session: Session,
):
    response: Response = client.get(f"/reviews/{recipe_in_db.id}/{review_in_db.id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == review_in_db.title
    assert response.json()["rating"] == review_in_db.rating


def test_authenticated_user_can_create_review(
    client: TestClient,
    review_data: dict[str, str | int],
    recipe_in_db: RecipeOutputSchema,
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.post(
        f"/reviews/{recipe_in_db.id}/",
        json=review_data,
        headers=user_bearer_token_header,
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert len(session.query(Review).all()) == 1
    assert session.query(Review).first().user_id == register_user.id
    assert response.json()["title"] == review_data["title"]
    assert response.json()["details"] == review_data["details"]


def test_authenticated_user_can_update_review(
    client: TestClient,
    review_in_db: ReviewOutputSchema,
    recipe_in_db: RecipeOutputSchema,
    review_update_data: dict[str, str | int],
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.put(
        f"/reviews/{recipe_in_db.id}/{review_in_db.id}/",
        json=review_update_data,
        headers=user_bearer_token_header,
    )
    assert response.status_code == status.HTTP_200_OK
    assert len(session.query(Review).all()) == 1
    assert response.json()["title"] == review_update_data["title"]
    assert response.json()["details"] == review_update_data["details"]


def test_other_user_cannot_update_review(
    client: TestClient,
    review_in_db: ReviewOutputSchema,
    recipe_in_db: RecipeOutputSchema,
    review_update_data: dict[str, str | int],
    other_user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.put(
        f"/reviews/{recipe_in_db.id}/{review_in_db.id}/",
        json=review_update_data,
        headers=other_user_bearer_token_header,
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "User is not owner of the review"
    assert (
        session.query(Review).filter_by(id=review_in_db.id).first().title
        == review_in_db.title
    )


def test_anonymous_user_cannot_create_review(
    client: TestClient,
    recipe_in_db: RecipeOutputSchema,
    review_data: dict[str, str | int],
    session: Session,
):
    response: Response = client.post(f"/reviews/{recipe_in_db.id}/", json=review_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


def test_anonymous_user_cannot_update_review(
    client: TestClient,
    review_in_db: ReviewOutputSchema,
    recipe_in_db: RecipeOutputSchema,
    review_update_data: dict[str, str | int],
    session: Session,
):
    response: Response = client.put(
        f"/reviews/{recipe_in_db.id}/{review_in_db.id}/", json=review_update_data
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"
    assert (
        session.query(Review).filter_by(id=review_in_db.id).first().title
        == review_in_db.title
    )
