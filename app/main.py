"""Main FastAPI application"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.api.recipes import router as recipes_router
from app.database import init_db
from app.config import PORT, HOST

# Initialize FastAPI app
app = FastAPI(
    title="Recipe Manager",
    description="Self-hosted recipe manager for ingesting and displaying recipes",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup templates
templates = Jinja2Templates(directory="templates")

# Include API routers
app.include_router(recipes_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"🍳 Recipe Manager started on http://{HOST}:{PORT}")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main web UI"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/recipes/{recipe_id}", response_class=HTMLResponse)
async def recipe_detail(request: Request, recipe_id: int):
    """Serve the recipe detail page"""
    return templates.TemplateResponse("recipe.html", {"request": request, "recipe_id": recipe_id})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
