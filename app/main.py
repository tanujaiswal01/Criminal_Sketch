from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import logging
from datetime import datetime
from db.session import engine
from db import models
from routes import auth, generation, case, witness, evidence, dashboard, user
from core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create default superuser
from service.auth import create_superuser
from db.session import SessionLocal

db = SessionLocal()
try:
    create_superuser(db)
finally:
    db.close()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Create static directory structure
static_dir = "static"
os.makedirs(static_dir, exist_ok=True)

# Serve static files
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(generation.router)
app.include_router(case.router)
app.include_router(witness.router)
app.include_router(evidence.router)
app.include_router(dashboard.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return {
        "message": "Portrait Generation API",
        "version": settings.PROJECT_VERSION,
        "description": "Generate portrait images from detailed physical descriptions",
        "endpoints": {
            "generate": "/generate-image",
            "auth": "/auth/token",
            "register": "/auth/register"
        }
    }

@app.get("/health")
async def health_check():
    """Check API health"""
    return {
        "status": "healthy",
        "api_version": settings.PROJECT_VERSION,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
