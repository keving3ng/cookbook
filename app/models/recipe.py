"""Recipe database model"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from app.database import Base


class Recipe(Base):
    """Recipe model for storing recipe data"""
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    ingredients = Column(JSON, nullable=False)  # Array of ingredient strings
    instructions = Column(JSON, nullable=False)  # Array of instruction strings
    prep_time = Column(Integer, nullable=True)  # Minutes
    cook_time = Column(Integer, nullable=True)  # Minutes
    servings = Column(Integer, nullable=True)
    images = Column(JSON, nullable=True)  # Array of image URLs
    tags = Column(JSON, nullable=True)  # Array of tag strings
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "id": self.id,
            "url": self.url,
            "title": self.title,
            "description": self.description,
            "ingredients": self.ingredients or [],
            "instructions": self.instructions or [],
            "prep_time": self.prep_time,
            "cook_time": self.cook_time,
            "servings": self.servings,
            "images": self.images or [],
            "tags": self.tags or [],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
