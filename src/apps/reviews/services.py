from uuid import UUID
from sqlalchemy import select, update, and_
from sqlalchemy.orm import Session
from src.apps.recipes.models import Recipe
from src.apps.reviews.models import Review
from src.apps.reviews.schemas import ReviewInputSchema, ReviewOutputSchema
from src.apps.users.models import User
from src.core.exceptions import (
    DoesNotExistException,
    InvalidUserException,
)


class ReviewService:
    @classmethod
    def _validate_user(cls, user: User, review: Review):
        if review.user != user:
            raise InvalidUserException("User is not owner of the review")

    @classmethod
    def get_review_list(
        cls,
        recipe_id: UUID,
        session: Session,
    ):
        return (
            session.execute(select(Review).where(Review.recipe_id == recipe_id))
            .scalars()
            .all()
        )

    @classmethod
    def get_review_by_id(
        cls,
        recipe_id: UUID,
        review_id: UUID,
        session: Session,
    ):
        review = (
            session.execute(
                select(Review).where(
                    and_(
                        Review.id == review_id,
                        Review.recipe_id == recipe_id,
                    )
                )
            )
            .scalars()
            .first()
        )
        if review is None:
            raise DoesNotExistException
        return review

    @classmethod
    def create_review(
        cls, schema: ReviewInputSchema, recipe_id: UUID, user: User, session: Session
    ) -> ReviewOutputSchema:
        review_data = schema.dict()
        recipe = (
            session.execute(select(Recipe).where(Recipe.id == recipe_id))
            .scalars()
            .first()
        )

        new_review = Review(**review_data, user=user, recipe=recipe)
        session.add(new_review)
        session.commit()
        session.refresh(new_review)
        return ReviewOutputSchema.from_orm(new_review)

    @classmethod
    def update_review(
        cls,
        schema: ReviewInputSchema,
        recipe_id: UUID,
        review_id: UUID,
        user: User,
        session: Session,
    ) -> Review:
        update_data = schema.dict()
        review = cls.get_review_by_id(
            recipe_id=recipe_id, review_id=review_id, session=session
        )
        cls._validate_user(user=user, review=review)

        session.execute(
            update(Review)
            .where(Review.id == review_id)
            .values(**update_data)
            .execution_options(synchronize_session="fetch")
        )
        return session.query(Review).filter_by(id=review_id).first()
