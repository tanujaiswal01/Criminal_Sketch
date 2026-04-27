import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Add app directory to path so we can import config if needed, 
# but here we just want to test the connection string from .env
sys.path.append(os.path.join(os.getcwd(), 'app'))

# Load .env explicitly
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("DB_PORT")

print(f"Testing connection to: postgresql://{DB_USER}:***@{DB_HOST}:{DB_PORT}/{DB_NAME}")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("Connection to image_gen_db successful!")
except Exception as e:
    print(f"Connection to {DB_NAME} failed: {e}")
    if 'database "' + DB_NAME + '" does not exist' in str(e):
        print(f"Database {DB_NAME} does not exist. Attempting to create it...")
        # Connect to default 'postgres' db to create the new db
        default_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
        try:
            from sqlalchemy.pool import NullPool
            # Use NullPool to avoid keeping connection open, and isolation_level="AUTOCOMMIT" for CREATE DATABASE
            engine_default = create_engine(default_url, isolation_level="AUTOCOMMIT", poolclass=NullPool)
            with engine_default.connect() as conn:
                conn.execute(text(f"CREATE DATABASE {DB_NAME}"))
                print(f"Successfully created database {DB_NAME}!")
            
            # Retry original connection
            engine = create_engine(DATABASE_URL)
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                print(f"Connection to {DB_NAME} successful after creation!")
        except Exception as create_error:
            print(f"Failed to create database: {create_error}")
            print("Please create the database manually using pgAdmin or psql.")
