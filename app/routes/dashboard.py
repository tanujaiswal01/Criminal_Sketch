from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db import session
from schema import dashboard as dashboard_schema
from service import dashboard as dashboard_service
from core.dependencies import get_current_user
from db.models import User

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"]
)

@router.get("/stats", response_model=dashboard_schema.DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get dashboard statistics including:
    
    - **active_cases**: Total number of active cases
    - **active_cases_change**: Number of active cases created this week
    - **urgent_cases**: Number of urgent priority cases
    - **pending_reviews**: Total cases pending review
    - **pending_reviews_due_today**: Cases with review due today
    - **cases_closed**: Total number of closed cases
    """
    return dashboard_service.get_dashboard_stats(db)

@router.get("/cases-by-status", response_model=List[dashboard_schema.CaseCountByStatus])
def get_cases_by_status(
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get case counts grouped by status.
    
    Returns a list of status counts (e.g., active, closed, pending, etc.)
    """
    return dashboard_service.get_cases_by_status(db)

@router.get("/cases-by-priority", response_model=List[dashboard_schema.CaseCountByPriority])
def get_cases_by_priority(
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get case counts grouped by priority.
    
    Returns a list of priority counts (low, normal, high, urgent)
    """
    return dashboard_service.get_cases_by_priority(db)
