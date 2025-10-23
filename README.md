# Recipe Manager

A self-hosted web application for ingesting recipes from URLs and displaying them in a clean, searchable interface. Single Docker container deployment for home server environments.

## Features

- **Recipe Ingestion**: Add recipes from any URL (supports major recipe sites)
- **Smart Parsing**: Uses JSON-LD schema.org/Recipe with HTML scraping fallback
- **Clean Interface**: Grid/card view with search functionality
- **Recipe Details**: Full recipe view with servings adjustment
- **Self-Hosted**: Single Docker container, no external dependencies
- **Persistent Storage**: SQLite database with volume mounting

## Quick Start

### Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone <repository-url>
cd cookbook
```

2. Start the application:
```bash
docker-compose up -d
```

3. Access the application at `http://localhost:3000`

### Using Docker

```bash
# Build the image
docker build -t recipe-manager .

# Run the container
docker run -d \
  -p 3000:3000 \
  -v ./data:/data \
  --name recipe-manager \
  recipe-manager
```

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file (optional):
```bash
cp .env.example .env
```

4. Run the application:
```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 3000
```

5. Access the application at `http://localhost:3000`

## Usage

### Adding Recipes

1. Navigate to the home page
2. Paste a recipe URL in the "Add New Recipe" form
3. Click "Add Recipe"
4. The recipe will be scraped and added to your collection

**Supported Sites**: Works with most major recipe websites including AllRecipes, Serious Eats, NYT Cooking, Food Network, and many more.

### Viewing Recipes

- Browse all recipes on the home page
- Use the search bar to find recipes by title or ingredient
- Click on a recipe card to view full details

### Recipe Details

- View complete ingredients and instructions
- Adjust serving sizes (ingredients automatically scale)
- Print-friendly view
- Link to original recipe source

### Deleting Recipes

- Click the "Delete" button on any recipe card
- Confirm deletion in the popup dialog

## API Documentation

Once the application is running, access the interactive API documentation at:
- Swagger UI: `http://localhost:3000/docs`
- ReDoc: `http://localhost:3000/redoc`

### API Endpoints

- `POST /api/recipes` - Add recipe from URL
- `GET /api/recipes` - List all recipes (with search/filter)
- `GET /api/recipes/{id}` - Get single recipe
- `DELETE /api/recipes/{id}` - Delete recipe
- `GET /health` - Health check endpoint

## Configuration

Environment variables (optional):

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | 3000 | Server port |
| `DATABASE_PATH` | /data/recipes.db | SQLite database path |

## Project Structure

```
cookbook/
├── app/
│   ├── api/
│   │   └── recipes.py       # Recipe API endpoints
│   ├── models/
│   │   └── recipe.py        # Recipe database model
│   ├── services/
│   │   └── scraper.py       # Recipe scraping service
│   ├── config.py            # Application configuration
│   ├── database.py          # Database connection
│   ├── main.py              # FastAPI application
│   └── schemas.py           # Pydantic schemas
├── static/
│   ├── css/
│   │   └── style.css        # Application styles
│   └── js/
│       └── app.js           # JavaScript utilities
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   └── recipe.html          # Recipe detail page
├── data/                    # Database storage (created at runtime)
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── PRD.md                   # Product requirements
├── README.md
└── requirements.txt
```

## Technical Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Scraping**: recipe-scrapers library
- **Frontend**: HTML/CSS with Alpine.js
- **Templating**: Jinja2
- **Container**: Docker

## Development

### Running Tests

```bash
# TODO: Add tests
pytest
```

### Database Migrations

Database schema is automatically created on first run. For schema changes:

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head
```

## Troubleshooting

### Recipe Won't Scrape

- Verify the URL is accessible
- Check if the site is supported by recipe-scrapers
- Some sites may block automated scraping
- Try accessing the recipe in a browser first

### Database Issues

- Ensure the `/data` directory has proper permissions
- Delete `data/recipes.db` to reset the database
- Check Docker volume mounts are configured correctly

### Port Already in Use

Change the port in docker-compose.yml or use a different port:
```bash
docker-compose run -p 8080:3000 recipe-manager
```

## Contributing

This is a personal project. Feel free to fork and modify for your needs.

## License

MIT License - See LICENSE file for details

## Roadmap

### Phase 2 - Enhanced UX
- [ ] Advanced search (fuzzy matching)
- [ ] Tag-based filtering
- [ ] Image caching/optimization
- [ ] Improved mobile experience

### Phase 3 - Polish
- [ ] Recipe export (PDF/JSON)
- [ ] Backup/restore functionality
- [ ] Bulk import from file
- [ ] Recipe editing after ingestion

### Future Considerations
- Manual recipe entry
- Meal planning features
- Shopping list generation
- Recipe notes and ratings
- Multi-user support with authentication

## Support

For issues, questions, or contributions, please open an issue on GitHub.
