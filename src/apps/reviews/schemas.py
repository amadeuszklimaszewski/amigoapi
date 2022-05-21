from uuid import UUID
from pydantic import BaseModel, Field


class ReviewInputSchema(BaseModel):
    title: str = Field(..., max_length=30)
    rating: int
    details: str


class ReviewOutputSchema(BaseModel):
    id: UUID
    tite: str
    user_id: UUID
    recipe_id: UUID
    rating: int
    details: str

    class Config:
        orm_mode = True
