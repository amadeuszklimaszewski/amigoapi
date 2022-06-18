from uuid import UUID
from typing import Any
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from src.apps.users.models import User
from src.apps.users.schemas import (
    UserRegisterSchema,
    UserUpdateSchema,
)
from src.apps.users.utils import pwd_context
from src.core.exceptions import (
    AlreadyExistsException,
    InvalidJWTUserException,
    PasswordMismatchException,
)


class UserService:
    @classmethod
    def _validate_password(cls, user_data: dict[str, Any]) -> None:
        if user_data["password"] != user_data["password2"]:
            raise PasswordMismatchException("Passwords do not match")

    @classmethod
    def _hash_password(cls, user_data: dict[str, Any]) -> None:
        password = user_data.pop("password2")
        user_data["password"] = pwd_context.hash(password)

    @classmethod
    def register_user(cls, schema: UserRegisterSchema, session: Session) -> User:
        user_data = schema.dict()
        cls._validate_password(user_data=user_data)
        cls._hash_password(user_data=user_data)

        if session.execute(
            select(User.email).where(User.email == user_data["email"])
        ).first():
            raise AlreadyExistsException("Email already in use!")
        if session.execute(
            select(User.username).where(User.username == user_data["username"])
        ).first():
            raise AlreadyExistsException("Username already taken!")

        new_user = User(**user_data)
        new_user.is_active = True

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    @classmethod
    def authenticate(cls, email: str, password: str, session: Session) -> User:
        user: User = (
            session.execute(select(User).where(User.email == email)).scalars().first()
        )
        if user is None or not pwd_context.verify(password, user.password):
            raise InvalidJWTUserException("No matches with given token")
        return user

    @classmethod
    def update_user(
        cls, user: User, schema: UserUpdateSchema, session: Session
    ) -> User:
        update_data = schema.dict()

        session.execute(
            update(User)
            .where(User.id == user.id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return session.execute(select(User).where(User.id == user.id)).scalars().first()

    @classmethod
    def get_user_list(
        cls,
        session: Session,
    ):
        return session.execute(select(User)).scalars().all()

    @classmethod
    def get_user_by_id(
        cls,
        user_id: UUID,
        session: Session,
    ):
        return session.execute(select(User).where(User.id == user_id)).scalars().first()
