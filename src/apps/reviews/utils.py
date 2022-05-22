from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.apps.recipes.models import Recipe
from src.apps.reviews.models import Review
from src.core.exceptions import InvalidRecipe


def validate_recipe(recipe_id: UUID, review_id: UUID, db: Session):
    recipe: Recipe = (
        db.execute(select(Recipe).where(Recipe.id == recipe_id)).scalars().first()
    )
    review: Review = (
        db.execute(select(Review).where(Review.id == review_id)).scalars().first()
    )

    if review.recipe != recipe:
        raise InvalidRecipe("Invalid recipe ID")
