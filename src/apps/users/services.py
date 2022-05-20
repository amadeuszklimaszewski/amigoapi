from typing import Any
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.apps.users.models import User
from src.apps.users.schemas import (
    UserOutputSchema,
    UserRegisterSchema,
    UserUpdateSchema,
)
from src.apps.users.utils import pwd_context
from src.core.exceptions import (
    AlreadyExists,
    InvalidJWTUser,
    PasswordMismatch,
)


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
        new_user.is_active = True

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return UserOutputSchema.from_orm(new_user)

    @classmethod
    def authenticate(cls, email: str, password: str, db: Session) -> User:
        user = db.query(User).filter_by(email=email).first()
        if user is None or not pwd_context.verify(password, user.password):
            raise InvalidJWTUser("No matches with given token")
        return user

    @classmethod
    def update_user(cls, user: User, schema: UserUpdateSchema, db: Session) -> User:
        update_data = schema.dict()

        db.execute(
            update(User)
            .where(User.id == user.id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return db.query(User).filter_by(id=user.id).first()
