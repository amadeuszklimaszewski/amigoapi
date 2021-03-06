from uuid import UUID
from fastapi.routing import APIRouter
from fastapi import Depends, status
from sqlalchemy.orm import Session
from src.apps.reviews.services import ReviewService
from src.apps.reviews.schemas import ReviewInputSchema, ReviewOutputSchema
from src.apps.users.models import User
from src.database.connection import get_db
from src.dependencies.users import authenticate_user


review_router = APIRouter(prefix="/reviews")


@review_router.get(
    "/{recipe_id}/",
    tags=["reviews"],
    status_code=status.HTTP_200_OK,
    response_model=list[ReviewOutputSchema],
)
def get_reviews(
    recipe_id: UUID,
    review_service: ReviewService = Depends(),
    session: Session = Depends(get_db),
) -> list[ReviewOutputSchema]:
    return [
        ReviewOutputSchema.from_orm(recipe)
        for recipe in review_service.get_review_list(
            recipe_id=recipe_id, session=session
        )
    ]


@review_router.get(
    "/{recipe_id}/{review_id}/",
    tags=["review"],
    status_code=status.HTTP_200_OK,
    response_model=ReviewOutputSchema,
)
def get_review_by_id(
    recipe_id: UUID,
    review_id: UUID,
    review_service: ReviewService = Depends(),
    session: Session = Depends(get_db),
) -> ReviewOutputSchema:
    review = review_service.get_review_by_id(
        recipe_id=recipe_id, review_id=review_id, session=session
    )
    return ReviewOutputSchema.from_orm(review)


@review_router.post(
    "/{recipe_id}/",
    tags=["reviews"],
    dependencies=[Depends(authenticate_user)],
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewOutputSchema,
)
def create_review(
    recipe_id: UUID,
    review_input_schema: ReviewInputSchema,
    review_service: ReviewService = Depends(),
    request_user: User = Depends(authenticate_user),
    session: Session = Depends(get_db),
) -> ReviewOutputSchema:
    review_schema = review_service.create_review(
        schema=review_input_schema,
        recipe_id=recipe_id,
        user=request_user,
        session=session,
    )
    return review_schema


@review_router.put(
    "/{recipe_id}/{review_id}/",
    tags=["recipes"],
    status_code=status.HTTP_200_OK,
    response_model=ReviewOutputSchema,
)
def update_review(
    recipe_id: UUID,
    review_id: UUID,
    update_schema: ReviewInputSchema,
    review_service: ReviewService = Depends(),
    request_user: User = Depends(authenticate_user),
    session: Session = Depends(get_db),
) -> ReviewOutputSchema:
    updated_review = review_service.update_review(
        schema=update_schema,
        recipe_id=recipe_id,
        review_id=review_id,
        user=request_user,
        session=session,
    )
    return ReviewOutputSchema.from_orm(updated_review)
