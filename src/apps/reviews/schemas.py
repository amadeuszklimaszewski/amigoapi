from uuid import UUID
from pydantic import BaseModel, Field, validator


class ReviewInputSchema(BaseModel):
    title: str = Field(..., max_length=30)
    rating: int
    details: str

    @validator("rating")
    def validate_rating(cls, rating: int) -> int:
        if rating > 10 or rating < 0:
            raise ValueError("Rating must be an integer between 0 and 10")
        return rating


class ReviewOutputSchema(BaseModel):
    id: UUID
    title: str
    user_id: UUID
    recipe_id: UUID
    rating: int
    details: str

    class Config:
        orm_mode = True
