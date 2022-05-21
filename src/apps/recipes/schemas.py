from uuid import UUID
from pydantic import BaseModel, Field


class RecipeInputSchema(BaseModel):
    title: str = Field(..., max_length=30)
    time_required: str
    servings: int
    description: str


class RecipeOutputSchema(BaseModel):
    id: UUID
    user_id: UUID
    title: str = Field(..., max_length=30)
    time_required: str
    servings: int
    description: str
    review_average: float | None
    review_count: int | None = Field(default=0)

    class Config:
        orm_mode = True
