from multiprocessing import synchronize
from uuid import UUID
from sqlalchemy import select, update
from sqlalchemy.orm import Session
from src.apps.recipes.models import Recipe
from src.apps.reviews.models import Review
from src.apps.reviews.schemas import ReviewInputSchema, ReviewOutputSchema
from src.apps.users.models import User
from src.core.exceptions import InvalidRecipe, InvalidUser


class ReviewService:
    @classmethod
    def _validate_user(cls, user: User, review: Review):
        if review.user != user:
            raise InvalidUser("User is not owner of the review")

    @classmethod
    def create_review(
        cls, schema: ReviewInputSchema, recipe_id: UUID, user: User, db: Session
    ) -> ReviewOutputSchema:
        review_data = schema.dict()
        recipe = (
            db.execute(select(Recipe).where(Recipe.id == recipe_id)).scalars().first()
        )

        new_review = Review(**review_data, user=user, recipe=recipe)
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return ReviewOutputSchema.from_orm(new_review)

    @classmethod
    def update_review(
        cls, schema: ReviewInputSchema, review_id: UUID, user: User, db: Session
    ) -> Review:
        update_data = schema.dict()
        review = (
            db.execute(select(Review).where(Review.id == review_id)).scalars().first()
        )
        cls._validate_user(user=user, review=review)

        db.execute(
            update(Review)
            .where(Review.id == review_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return db.query(Review).filter_by(id=review_id).first()
