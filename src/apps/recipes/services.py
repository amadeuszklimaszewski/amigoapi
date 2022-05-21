from multiprocessing import synchronize
from typing import Any
from uuid import UUID
from sqlalchemy import update
from sqlalchemy.orm import Session

from src.apps.recipes.models import Recipe
from src.apps.recipes.schemas import RecipeInputSchema, RecipeOutputSchema
from src.apps.users.models import User


class RecipeService:
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
        cls, recipe_id: UUID, schema: RecipeInputSchema, db: Session
    ) -> Recipe:
        print(schema)
        update_data = schema.dict()

        db.execute(
            update(Recipe)
            .where(Recipe.id == recipe_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return db.query(Recipe).filter_by(id=recipe_id).first()
