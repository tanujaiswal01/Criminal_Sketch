from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import models
from schema import user as user_schema
from core import security

def register_user(db: Session, user: user_schema.UserCreate, role: str = "user"):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_email = db.query(models.User).filter(models.User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password,
        role=role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def create_superuser(db: Session):
    from core.config import settings
    user = db.query(models.User).filter(models.User.email == settings.FIRST_SUPERUSER).first()
    if not user:
        user_in = user_schema.UserCreate(
            email=settings.FIRST_SUPERUSER,
            username=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD
        )
        register_user(db, user_in, role="officer")

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return False
    if not security.verify_password(password, user.hashed_password):
        return False
    return user
