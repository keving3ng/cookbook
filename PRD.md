# Recipe Manager - Product Requirements Document

## Overview
Self-hosted web application for ingesting recipes from URLs and displaying them in a clean, searchable interface. Single Docker container deployment for home server environments.

## Core Functionality

### 1. Recipe Ingestion
**Input**: URL to recipe webpage
**Process**:
- Extract recipe data (title, ingredients, instructions, prep/cook time, servings, images)
- Parse using structured data (JSON-LD schema.org/Recipe) or HTML scraping fallback
- Store in local database

**Acceptance Criteria**:
- Successfully parse recipes from major sites (AllRecipes, Serious Eats, NYT Cooking, Food Network, etc.)
- Handle missing fields gracefully (optional: prep time, images, etc.)
- Duplicate detection (same URL won't create multiple entries)
- Basic validation (must have title + ingredients or instructions)

### 2. Recipe Display
**Features**:
- Grid/card view of all recipes (thumbnail, title, quick stats)
- Individual recipe page (full details, scaled servings)
- Search by title/ingredient
- Filter by tags (auto-generated from ingredients/categories)
- Responsive design (mobile-friendly)

**Acceptance Criteria**:
- Clean, readable recipe view
- Search returns results in <1s for 1000+ recipes
- Servings adjustment recalculates ingredient quantities
- Print-friendly view

## Technical Architecture

### Stack
- **Backend**: Python/FastAPI or Node/Express
- **Frontend**: Static HTML/CSS/JS (Alpine.js or HTMX for interactivity)
- **Database**: SQLite or PostgreSQL
- **Scraping**: Recipe-scrapers library (Python) or custom parser
- **Container**: Single Docker image with all dependencies

### Data Model
```
Recipe:
  - id (primary key)
  - url (unique)
  - title
  - description
  - ingredients (JSON array)
  - instructions (JSON array/text)
  - prep_time (minutes, nullable)
  - cook_time (minutes, nullable)
  - servings (number)
  - images (JSON array of URLs)
  - tags (JSON array)
  - created_at
  - updated_at
```

### API Endpoints
```
POST   /api/recipes          - Add recipe from URL
GET    /api/recipes          - List all recipes (with search/filter params)
GET    /api/recipes/:id      - Get single recipe
DELETE /api/recipes/:id      - Delete recipe
GET    /                     - Web UI
```

## Deployment

### Docker Setup
```yaml
# Single container includes:
- Web server
- Application backend
- Database (volume-mounted for persistence)
- Static frontend assets
```

**Environment Variables**:
- `PORT` (default: 3000)
- `DATABASE_PATH` (default: /data/recipes.db)

**Volumes**:
- `/data` - Database and uploaded images persistence

**Run Command**:
```bash
docker run -d \
  -p 3000:3000 \
  -v ./data:/data \
  recipe-manager:latest
```

## Development Priorities

### Phase 1 - MVP (Week 1)
- [ ] Recipe scraper (Python recipe-scrapers library)
- [ ] SQLite database with Recipe model
- [ ] REST API (add, list, get, delete)
- [ ] Basic HTML frontend (add URL form, recipe list, recipe detail page)
- [ ] Dockerfile with all dependencies

### Phase 2 - Enhanced UX (Week 2)
- [ ] Search functionality (title + ingredients)
- [ ] Tag extraction and filtering
- [ ] Servings scaling calculator
- [ ] Responsive CSS (mobile-friendly)
- [ ] Image handling (download/cache or hotlink)

### Phase 3 - Polish (Week 3)
- [ ] Error handling (invalid URLs, scraping failures)
- [ ] Loading states and user feedback
- [ ] Print stylesheet
- [ ] Recipe export (PDF/JSON)
- [ ] Backup/restore functionality

## Non-Functional Requirements

### Performance
- Recipe ingestion: <5s for most sites
- Page load: <500ms
- Search results: <1s for 1000+ recipes

### Reliability
- Graceful degradation when scraping fails
- Data persistence across container restarts
- Database automatic backups (via volume)

### Security
- Basic input validation (URL format)
- SQL injection prevention (parameterized queries)
- No authentication required (trusted local network assumed)

## Out of Scope (v1)
- User authentication/multi-user support
- Manual recipe entry (URL-only for MVP)
- Recipe editing after ingestion
- Meal planning features
- Shopping list generation
- Recipe ratings/notes
- Social features (sharing, comments)

## Success Metrics
- Successfully parse 90%+ of recipes from top 20 recipe sites
- Single command deployment (`docker run`)
- Recipe displayed within 1 click from home page
- Zero-config setup (works immediately after deployment)

## Technical Constraints
- Single Docker container (no orchestration required)
- Minimal resource usage (<512MB RAM, <1GB disk for 1000 recipes)
- No external API dependencies (self-contained)
- Works offline after recipe ingestion

## Reference Implementation
Python stack recommendation:
- FastAPI (async API framework)
- recipe-scrapers (battle-tested parser library)
- SQLAlchemy (ORM)
- SQLite (zero-config database)
- Jinja2 (templating)
- Alpine.js (minimal JS framework)
