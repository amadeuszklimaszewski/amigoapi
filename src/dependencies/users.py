import json

from fastapi import Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from src.core.exceptions import InvalidCredentialsException
from src.apps.users.models import User
from src.database.connection import get_db


def authenticate_user(
    auth_jwt: AuthJWT = Depends(), db: Session = Depends(get_db)
) -> User:
    auth_jwt.jwt_required()
    user = json.loads(auth_jwt.get_jwt_subject())
    user = db.query(User).filter_by(id=user["id"]).first()

    if user is None:
        raise InvalidCredentialsException("Invalid credentials provided.")

    return user
