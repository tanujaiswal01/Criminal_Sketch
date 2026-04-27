import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = "Portrait Generation API"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_USER: str = os.getenv("POSTGRES_USER", "postgres")
    DB_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "Jaiswal123")
    DB_NAME: str = os.getenv("POSTGRES_DB", "image_gen_db")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 720
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 1440  # 1 day in minutes

    # AI Clients
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")

    # Default Admin
    FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "officer@example.com")
    FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "officer123")
    FIRST_SUPERUSER_USERNAME: str = os.getenv("FIRST_SUPERUSER_USERNAME", "officer")

settings = Settings()
