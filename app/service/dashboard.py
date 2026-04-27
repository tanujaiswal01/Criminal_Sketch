from sqlalchemy.orm import Session
from sqlalchemy import func
from db import models
from schema import dashboard as dashboard_schema
from datetime import datetime, timedelta
from typing import List

def get_dashboard_stats(db: Session) -> dashboard_schema.DashboardStats:
    """Get dashboard statistics"""
    
    # Active cases (status = 'active')
    active_cases = db.query(models.Case).filter(models.Case.status == "active").count()
    
    # Active cases created this week
    week_ago = datetime.now() - timedelta(days=7)
    active_cases_this_week = db.query(models.Case).filter(
        models.Case.status == "active",
        models.Case.created_at >= week_ago
    ).count()
    
    # Urgent cases (priority = 'urgent' and status = 'active')
    urgent_cases = db.query(models.Case).filter(
        models.Case.priority == "urgent",
        models.Case.status == "active"
    ).count()
    
    # Pending reviews (cases with review_due_date set and status = 'active')
    pending_reviews = db.query(models.Case).filter(
        models.Case.review_due_date.isnot(None),
        models.Case.status == "active"
    ).count()
    
    # Pending reviews due today
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    pending_reviews_due_today = db.query(models.Case).filter(
        models.Case.review_due_date >= today_start,
        models.Case.review_due_date < today_end,
        models.Case.status == "active"
    ).count()
    
    # Cases closed (status = 'closed')
    cases_closed = db.query(models.Case).filter(models.Case.status == "closed").count()
    
    return dashboard_schema.DashboardStats(
        active_cases=active_cases,
        active_cases_change=active_cases_this_week,
        urgent_cases=urgent_cases,
        pending_reviews=pending_reviews,
        pending_reviews_due_today=pending_reviews_due_today,
        cases_closed=cases_closed
    )

def get_cases_by_status(db: Session) -> List[dashboard_schema.CaseCountByStatus]:
    """Get case counts grouped by status"""
    results = db.query(
        models.Case.status,
        func.count(models.Case.id).label('count')
    ).group_by(models.Case.status).all()
    
    return [
        dashboard_schema.CaseCountByStatus(status=status, count=count)
        for status, count in results
    ]

def get_cases_by_priority(db: Session) -> List[dashboard_schema.CaseCountByPriority]:
    """Get case counts grouped by priority"""
    results = db.query(
        models.Case.priority,
        func.count(models.Case.id).label('count')
    ).group_by(models.Case.priority).all()
    
    return [
        dashboard_schema.CaseCountByPriority(priority=priority, count=count)
        for priority, count in results
    ]
