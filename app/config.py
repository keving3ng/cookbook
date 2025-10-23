"""Application configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Server Configuration
PORT = int(os.getenv("PORT", "3000"))
HOST = os.getenv("HOST", "0.0.0.0")

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/recipes.db")

# Ensure data directory exists
data_dir = Path(DATABASE_PATH).parent
data_dir.mkdir(parents=True, exist_ok=True)

# Database URL for SQLAlchemy
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
