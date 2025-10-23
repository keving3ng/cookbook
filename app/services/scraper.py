"""Recipe scraping service"""
from typing import Dict, Any, Optional
from recipe_scrapers import scrape_me
import re


class RecipeScraperService:
    """Service for scraping recipe data from URLs"""

    @staticmethod
    def scrape_recipe(url: str) -> Dict[str, Any]:
        """
        Scrape recipe data from a URL

        Args:
            url: URL of the recipe page

        Returns:
            Dictionary containing recipe data

        Raises:
            ValueError: If URL is invalid or recipe cannot be scraped
        """
        # Validate URL format
        if not RecipeScraperService._is_valid_url(url):
            raise ValueError("Invalid URL format")

        try:
            # Use recipe-scrapers library
            scraper = scrape_me(url, wild_mode=True)

            # Extract recipe data
            recipe_data = {
                "url": url,
                "title": RecipeScraperService._safe_get(scraper.title),
                "description": RecipeScraperService._safe_get(scraper.description),
                "ingredients": RecipeScraperService._safe_get(scraper.ingredients, []),
                "instructions": RecipeScraperService._safe_get_instructions(scraper),
                "prep_time": RecipeScraperService._safe_get_time(scraper.prep_time),
                "cook_time": RecipeScraperService._safe_get_time(scraper.cook_time),
                "servings": RecipeScraperService._safe_get_servings(scraper.yields),
                "images": RecipeScraperService._safe_get_images(scraper.image),
                "tags": RecipeScraperService._extract_tags(scraper),
            }

            # Validate minimum required fields
            if not recipe_data["title"]:
                raise ValueError("Recipe must have a title")

            if not recipe_data["ingredients"] and not recipe_data["instructions"]:
                raise ValueError("Recipe must have ingredients or instructions")

            return recipe_data

        except Exception as e:
            raise ValueError(f"Failed to scrape recipe: {str(e)}")

    @staticmethod
    def _is_valid_url(url: str) -> bool:
        """Validate URL format"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return url_pattern.match(url) is not None

    @staticmethod
    def _safe_get(func, default=None):
        """Safely call a scraper function"""
        try:
            result = func() if callable(func) else func
            return result if result else default
        except:
            return default

    @staticmethod
    def _safe_get_instructions(scraper) -> list:
        """Safely get instructions as list"""
        try:
            instructions = scraper.instructions()
            if isinstance(instructions, str):
                # Split by newlines and clean up
                return [line.strip() for line in instructions.split('\n') if line.strip()]
            elif isinstance(instructions, list):
                return instructions
            return []
        except:
            return []

    @staticmethod
    def _safe_get_time(time_func) -> Optional[int]:
        """Safely get time in minutes"""
        try:
            time_val = time_func()
            if isinstance(time_val, int):
                return time_val
            return None
        except:
            return None

    @staticmethod
    def _safe_get_servings(yields_func) -> Optional[int]:
        """Safely extract servings number"""
        try:
            yields_val = yields_func()
            if isinstance(yields_val, int):
                return yields_val
            if isinstance(yields_val, str):
                # Try to extract number from string like "4 servings"
                match = re.search(r'\d+', yields_val)
                if match:
                    return int(match.group())
            return None
        except:
            return None

    @staticmethod
    def _safe_get_images(image_func) -> list:
        """Safely get images as list"""
        try:
            image = image_func()
            if image:
                return [image] if isinstance(image, str) else list(image)
            return []
        except:
            return []

    @staticmethod
    def _extract_tags(scraper) -> list:
        """Extract tags from recipe metadata"""
        tags = []
        try:
            # Try to get category
            category = RecipeScraperService._safe_get(scraper.category)
            if category:
                tags.append(category)

            # Try to get cuisine
            cuisine = RecipeScraperService._safe_get(scraper.cuisine)
            if cuisine:
                tags.append(cuisine)
        except:
            pass

        return tags
