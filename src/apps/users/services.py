from typing import Any
from sqlalchemy.orm import Session

from src.apps.users.models import User
from src.apps.users.schemas import UserOutputSchema, UserRegisterSchema
from src.apps.users.utils import pwd_context
from src.core.exceptions import AlreadyExists, PasswordMismatch


class UserService:
    @classmethod
    def _validate_password(cls, user_data: dict[str, Any]) -> None:
        if user_data["password"] != user_data["password2"]:
            raise PasswordMismatch("Passwords do not match")

    @classmethod
    def _hash_password(cls, user_data: dict[str, Any]) -> None:
        password = user_data.pop("password2")
        user_data["password"] = pwd_context.hash(password)

    @classmethod
    def register_user(cls, schema: UserRegisterSchema, db: Session) -> UserOutputSchema:
        user_data = schema.dict()
        cls._validate_password(user_data=user_data)
        cls._hash_password(user_data=user_data)

        if db.query(User.email).filter_by(email=user_data["email"]).first():
            raise AlreadyExists("Email already in use!")
        if db.query(User.username).filter_by(username=user_data["username"]).first():
            raise AlreadyExists("Username already taken!")

        new_user = User(**user_data)

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOutputSchema.from_orm(new_user)
