import pytest
from fastapi import Response, status
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from src.apps.users.schemas import UserOutputSchema

from src.apps.users.models import User


@pytest.fixture
def user_update_data() -> dict[str, str]:
    return {
        "first_name": "update",
        "last_name": "update",
        "email": "update@google.com",
    }


@pytest.fixture
def user_login_data(user_register_data: dict[str, str]) -> dict[str, str]:
    return {
        "email": user_register_data["email"],
        "password": user_register_data["password"],
    }


def test_user_can_login(
    client: TestClient,
    register_user: UserOutputSchema,
    user_login_data: dict[str, str],
    session: Session,
):
    response: Response = client.post("/users/login/", json=user_login_data)

    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert len(response_body) == 1


def test_user_can_register(
    client: TestClient,
    user_register_data: dict[str, str],
    session: Session,
):
    response: Response = client.post("/users/register/", json=user_register_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert len(session.query(User).all()) == 1
    assert session.query(User).first().username == user_register_data["username"]


def test_authenticated_user_can_get_users_list(
    client: TestClient,
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.get("/users/", headers=user_bearer_token_header)
    assert response.status_code == status.HTTP_200_OK

    response_body = response.json()
    assert len(response_body) == 1


def test_authenticated_user_can_get_his_profile(
    client: TestClient,
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.get("/users/profile", headers=user_bearer_token_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == register_user.username
    assert response.json()["id"] == str(register_user.id)


def test_authenticated_user_can_get_his_profile_by_id(
    client: TestClient,
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.get(
        f"/users/{register_user.id}", headers=user_bearer_token_header
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == register_user.username
    assert response.json()["id"] == str(register_user.id)


def test_authenticated_user_can_update_his_profile(
    client: TestClient,
    user_update_data: dict[str, str],
    register_user: UserOutputSchema,
    user_bearer_token_header: dict[str, str],
    session: Session,
):
    response: Response = client.put(
        "/users/profile/",
        headers=user_bearer_token_header,
        json=user_update_data,
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["first_name"] == user_update_data["first_name"]
    assert response.json()["email"] == user_update_data["email"]
    assert response.json()["id"] == str(register_user.id)


def test_anonymous_user_cannot_get_users_list(
    client: TestClient,
    register_user: UserOutputSchema,
    session: Session,
):
    response: Response = client.get("/users/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


def test_anonymous_user_cannot_get_users_profile(
    client: TestClient,
    register_user: UserOutputSchema,
    session: Session,
):
    response: Response = client.get("/users/profile/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


def test_anonymous_user_cannot_get_users_profile_by_id(
    client: TestClient,
    register_user: UserOutputSchema,
    session: Session,
):
    response: Response = client.get(f"/users/{register_user.id}/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"


def test_anonymous_user_cannot_update_users_profile(
    client: TestClient,
    register_user: UserOutputSchema,
    user_update_data: dict[str, str],
    session: Session,
):
    response: Response = client.put(f"/users/profile/", json=user_update_data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    response_body = response.json()
    assert len(response_body) == 1
    assert response_body["detail"] == "Missing Authorization Header"
