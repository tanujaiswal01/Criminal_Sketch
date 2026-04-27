from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CaseBase(BaseModel):
    case_name: str
    case_details: str
    investigator: str
    status: Optional[str] = "active"
    priority: Optional[str] = "normal"  # low, normal, high, urgent
    review_due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None  # User ID of assigned investigator

class CaseCreate(CaseBase):
    pass

class CaseUpdate(BaseModel):
    case_name: Optional[str] = None
    case_details: Optional[str] = None
    investigator: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    review_due_date: Optional[datetime] = None
    assigned_to: Optional[int] = None

class CaseResponse(CaseBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
