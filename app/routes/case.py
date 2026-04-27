from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db import session
from schema import case as case_schema
from service import case as case_service
from core.dependencies import get_current_user
from db.models import User

router = APIRouter(
    prefix="/cases",
    tags=["cases"]
)

@router.post("/create_case", response_model=case_schema.CaseResponse, status_code=status.HTTP_201_CREATED)
def create_case(
    case: case_schema.CaseCreate,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new case.
    
    - **case_name**: Name of the case
    - **case_details**: Detailed description of the case
    - **investigator**: Name of the investigator assigned
    - **status**: Case status (default: active)
    - **assigned_to**: User ID of investigator assigned to this case
    """
    return case_service.create_case(db, case, current_user.id)

@router.get("/", response_model=List[case_schema.CaseResponse])
def get_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status (e.g., 'active', 'closed')"),
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get cases based on user role:
    - Officers: See all cases
    - Investigators: See only cases assigned to them
    - Users: See only cases they created
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter cases by status
    """
    return case_service.get_cases(db, current_user, skip, limit, status)

@router.get("/{case_id}", response_model=case_schema.CaseResponse)
def get_case(
    case_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific case by ID.
    """
    return case_service.get_case(db, case_id)

@router.put("/{case_id}", response_model=case_schema.CaseResponse)
def update_case(
    case_id: int,
    case_update: case_schema.CaseUpdate,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a case.
    
    You can update any of the following fields:
    - **case_name**
    - **case_details**
    - **investigator**
    - **status**
    - **assigned_to**
    """
    return case_service.update_case(db, case_id, case_update, current_user.id)

@router.delete("/{case_id}")
def delete_case(
    case_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a case.
    """
    return case_service.delete_case(db, case_id, current_user.id)
