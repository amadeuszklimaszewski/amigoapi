import uuid

from sqlalchemy import Column, String, Boolean, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from src.database.connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    email = Column(String, unique=True)
    username = Column(String(length=50), unique=True)
    first_name = Column(String(length=50))
    last_name = Column(String(length=50))
    birthday = Column(Date)
    password = Column(String)
    is_active = Column(Boolean, default=False)

    recipes = relationship("Recipe", back_populates="user")
    reviews = relationship("Review", back_populates="user")
