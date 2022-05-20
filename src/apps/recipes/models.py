import uuid

from sqlalchemy import select, func
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import column_property
from sqlalchemy.dialects.postgresql import UUID

from src.database.connection import Base
from src.apps.reviews.models import Review


class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    title = Column(String(30))
    time_required = Column(String)
    servings = Column(Integer)
    description = Column(Text)

    review_average = column_property(
        select(func.avg(Review.rating))
        .where(Review.recipe_id == id)
        .correlate_except(Review)
        .scalar_subquery()
    )
    review_count = column_property(
        select(func.count(Review.id))
        .where(Review.recipe_id == id)
        .correlate_except(Review)
        .scalar_subquery()
    )
