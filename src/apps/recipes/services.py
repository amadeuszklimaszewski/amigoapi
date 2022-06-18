from multiprocessing import synchronize
from typing import Any
from uuid import UUID
from sqlalchemy import update, select
from sqlalchemy.orm import Session

from src.core.exceptions import InvalidUser
from src.apps.recipes.models import Recipe
from src.apps.recipes.schemas import RecipeInputSchema, RecipeOutputSchema
from src.apps.users.models import User


class RecipeService:
    @classmethod
    def _validate_user(cls, user: User, recipe: Recipe):
        if recipe.user != user:
            raise InvalidUser("User is not owner of the recipe")

    @classmethod
    def create_recipe(
        cls, schema: RecipeInputSchema, user: User, db: Session
    ) -> RecipeOutputSchema:
        recipe_data = schema.dict()
        new_recipe = Recipe(**recipe_data, user=user)
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)
        return RecipeOutputSchema.from_orm(new_recipe)

    @classmethod
    def update_recipe(
        cls, recipe_id: UUID, user: User, schema: RecipeInputSchema, db: Session
    ) -> Recipe:
        update_data = schema.dict()
        recipe = (
            db.execute(select(Recipe).where(Recipe.id == recipe_id)).scalars().first()
        )
        cls._validate_user(user=user, recipe=recipe)
        db.execute(
            update(Recipe)
            .where(Recipe.id == recipe_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return (
            db.execute(select(Recipe).where(Recipe.id == recipe_id)).scalars().first()
        )
