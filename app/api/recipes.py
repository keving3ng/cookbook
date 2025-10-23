"""Recipe API endpoints"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.database import get_db
from app.models.recipe import Recipe
from app.schemas import RecipeCreate, RecipeResponse, RecipeList, ErrorResponse
from app.services.scraper import RecipeScraperService

router = APIRouter(prefix="/api/recipes", tags=["recipes"])


@router.post("", response_model=RecipeResponse, status_code=201)
async def create_recipe(
    recipe_data: RecipeCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new recipe by scraping from URL

    - Checks for duplicate URLs
    - Scrapes recipe data from the provided URL
    - Stores in database
    """
    # Check if URL already exists
    existing = db.query(Recipe).filter(Recipe.url == recipe_data.url).first()
    if existing:
        raise HTTPException(status_code=409, detail="Recipe with this URL already exists")

    # Scrape recipe data
    try:
        scraped_data = RecipeScraperService.scrape_recipe(recipe_data.url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape recipe: {str(e)}")

    # Create recipe in database
    db_recipe = Recipe(**scraped_data)
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)

    return db_recipe


@router.get("", response_model=RecipeList)
async def list_recipes(
    search: Optional[str] = Query(None, description="Search in title and ingredients"),
    tag: Optional[str] = Query(None, description="Filter by tag"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """
    List all recipes with optional search and filtering

    - Search by title or ingredients
    - Filter by tags
    - Pagination support
    """
    query = db.query(Recipe)

    # Apply search filter
    if search:
        search_filter = or_(
            Recipe.title.ilike(f"%{search}%"),
            Recipe.ingredients.cast(str).ilike(f"%{search}%")
        )
        query = query.filter(search_filter)

    # Apply tag filter
    if tag:
        query = query.filter(Recipe.tags.cast(str).ilike(f"%{tag}%"))

    # Get total count
    total = query.count()

    # Apply pagination
    recipes = query.order_by(Recipe.created_at.desc()).offset(skip).limit(limit).all()

    return RecipeList(recipes=recipes, total=total)


@router.get("/{recipe_id}", response_model=RecipeResponse)
async def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Get a single recipe by ID
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.delete("/{recipe_id}", status_code=204)
async def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    """
    Delete a recipe by ID
    """
    recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    db.delete(recipe)
    db.commit()
    return None
