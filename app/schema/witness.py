from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class WitnessBase(BaseModel):
    name: str
    contact: str  # Email or phone number
    statement_date: datetime
    status: Optional[str] = "pending"  # pending, interviewed, follow-up
    protection: Optional[str] = "none"  # none, required, active
    case_id: Optional[int] = None
    is_anonymous: Optional[bool] = False

class WitnessCreate(WitnessBase):
    pass

class WitnessUpdate(BaseModel):
    name: Optional[str] = None
    contact: Optional[str] = None
    statement_date: Optional[datetime] = None
    status: Optional[str] = None
    protection: Optional[str] = None
    case_id: Optional[int] = None
    is_anonymous: Optional[bool] = None

class WitnessResponse(WitnessBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
