from multiprocessing import synchronize
from typing import Any
from uuid import UUID
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from src.core.exceptions import InvalidUserException
from src.apps.recipes.models import Recipe
from src.apps.recipes.schemas import RecipeInputSchema
from src.apps.users.models import User


class RecipeService:
    @classmethod
    def _validate_user(cls, user: User, recipe: Recipe):
        if recipe.user != user:
            raise InvalidUserException("User is not owner of the recipe")

    @classmethod
    def get_recipe_list(
        cls,
        session: Session,
    ):
        return session.execute(select(Recipe)).scalars().all()

    @classmethod
    def get_recipe_by_id(
        cls,
        recipe_id: UUID,
        session: Session,
    ):
        return (
            session.execute(select(Recipe).where(Recipe.id == recipe_id))
            .scalars()
            .first()
        )

    @classmethod
    def create_recipe(
        cls, schema: RecipeInputSchema, user: User, session: Session
    ) -> Recipe:
        recipe_data = schema.dict()
        new_recipe = Recipe(**recipe_data, user=user)
        session.add(new_recipe)
        session.commit()
        session.refresh(new_recipe)
        return new_recipe

    @classmethod
    def update_recipe(
        cls, recipe_id: UUID, user: User, schema: RecipeInputSchema, session: Session
    ) -> Recipe:
        update_data = schema.dict()
        recipe = (
            session.execute(select(Recipe).where(Recipe.id == recipe_id))
            .scalars()
            .first()
        )
        cls._validate_user(user=user, recipe=recipe)
        session.execute(
            update(Recipe)
            .where(Recipe.id == recipe_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return (
            session.execute(select(Recipe).where(Recipe.id == recipe_id))
            .scalars()
            .first()
        )
