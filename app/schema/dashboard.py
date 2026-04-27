from pydantic import BaseModel
from typing import Optional

class DashboardStats(BaseModel):
    active_cases: int
    active_cases_change: int  # Change this week
    urgent_cases: int
    pending_reviews: int
    pending_reviews_due_today: int
    cases_closed: int

class CaseCountByStatus(BaseModel):
    status: str
    count: int

class CaseCountByPriority(BaseModel):
    priority: str
    count: int
