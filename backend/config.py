import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Fallback to sqlite if DATABASE_URI is not set in .env
    default_db = f"sqlite:///{os.path.join(BASE_DIR, 'database', 'database.db')}"
    
    # SQLAlchemy requires 'postgresql://' instead of 'postgres://'
    # Supabase gives you postgresql:// URI so it should work out of the box
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', default_db)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'super-secret-jwt-key-for-certifyme')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'app-secret-key-for-certifyme')
