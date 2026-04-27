from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db import session, models
from schema import user as user_schema
from core.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/investigators", response_model=List[user_schema.UserResponse])
def get_investigators(
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all users with the 'investigator' role.
    This endpoint is useful for assigning cases to investigators.
    """
    investigators = db.query(models.User).filter(
        models.User.role == "investigator",
        models.User.is_active == True
    ).all()
    
    return investigators

@router.get("/", response_model=List[user_schema.UserResponse])
def get_all_users(
    db: Session = Depends(session.get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Get all users. Only accessible by officers.
    """
    # Only officers can view all users
    if current_user.role != "officer":
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only officers can view all users"
        )
    
    users = db.query(models.User).all()
    return users
