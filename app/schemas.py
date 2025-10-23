"""Pydantic schemas for API validation"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class RecipeCreate(BaseModel):
    """Schema for creating a recipe from URL"""
    url: str


class RecipeResponse(BaseModel):
    """Schema for recipe response"""
    id: int
    url: str
    title: str
    description: Optional[str] = None
    ingredients: List[str] = []
    instructions: List[str] = []
    prep_time: Optional[int] = None
    cook_time: Optional[int] = None
    servings: Optional[int] = None
    images: List[str] = []
    tags: List[str] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class RecipeList(BaseModel):
    """Schema for list of recipes"""
    recipes: List[RecipeResponse]
    total: int


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
