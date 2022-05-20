import uuid

from sqlalchemy import select, func
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Integer
from sqlalchemy.orm import column_property, relationship
from sqlalchemy.dialects.postgresql import UUID

from src.database.connection import Base


class Review(Base):
    __tablename__ = "reviews"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    recipe_id = Column(UUID(as_uuid=True), ForeignKey("recipes.id"))
    title = Column(String)
    rating = Column(Integer)
    details = Column(Text)

    user = relationship("User", back_populates="reviews")
    recipe = relationship("Recipe", back_populates="reviews")
