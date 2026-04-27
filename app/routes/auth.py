from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from db import session
from schema import user as user_schema
from service import auth as auth_service
from core import security, config
from core.dependencies import get_current_active_superuser
from jose import jwt

router = APIRouter(
    prefix="/auth",
    tags=["authentication"]
)

@router.post("/register", response_model=user_schema.UserResponse)
def register(user: user_schema.UserCreate, db: Session = Depends(session.get_db)):
    return auth_service.register_user(db, user, role="user")

@router.post("/create-user", response_model=user_schema.UserResponse)
def create_user(
    user: user_schema.UserCreateWithRole, 
    db: Session = Depends(session.get_db),
    # current_user: user_schema.UserResponse = Depends(get_current_active_superuser)
):
    """
    Create a new user with a specific role. Only accessible by officers.
    
    Available roles:
    - user: Regular user
    - investigator: Investigator with case management access
    - officer: Officer with full administrative privileges
    """
    return auth_service.register_user(db, user, role=user.role)

@router.post("/token", response_model=user_schema.Token)
def login_for_access_token(
    login_data: user_schema.UserLogin,
    db: Session = Depends(session.get_db)
):
    """
    Login endpoint that returns access token, refresh token, and user information.
    """
    user = auth_service.authenticate_user(db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=config.settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    refresh_token = security.create_refresh_token(data={"sub": user.username}, expires_delta=refresh_token_expires)
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role,
            "is_active": user.is_active
        }
    }

@router.post("/refresh-token", response_model=user_schema.Token)
def refresh_access_token(
    refresh_data: user_schema.TokenRefreshRequest,
    db: Session = Depends(session.get_db)
):
    """
    Refresh access token using a valid refresh token.
    """
    try:
        payload = jwt.decode(
            refresh_data.refresh_token,
            config.settings.SECRET_KEY,
            algorithms=[config.settings.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
            )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = security.create_access_token(data={"sub": username}, expires_delta=access_token_expires)
    return {"access_token": new_access_token, "token_type": "bearer"}
