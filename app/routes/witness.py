from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db import session
from schema import witness as witness_schema
from service import witness as witness_service
from core.dependencies import get_current_user
from db.models import User

router = APIRouter(
    prefix="/witnesses",
    tags=["witnesses"]
)

@router.post("/", response_model=witness_schema.WitnessResponse, status_code=status.HTTP_201_CREATED)
def create_witness(
    witness: witness_schema.WitnessCreate,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new witness.
    
    - **name**: Full name of the witness (can be "Anonymous Witness #X" for anonymous)
    - **contact**: Email or phone number (can be "Confidential" for anonymous)
    - **statement_date**: Date when statement was taken
    - **status**: Witness status (pending, interviewed, follow-up)
    - **protection**: Protection level (none, required, active)
    - **case_id**: Optional case ID to link witness to a case
    - **is_anonymous**: Whether the witness is anonymous
    """
    return witness_service.create_witness(db, witness, current_user.id)

@router.get("/", response_model=List[witness_schema.WitnessResponse])
def get_witnesses(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[str] = Query(None, description="Filter by status (pending, interviewed, follow-up)"),
    protection: Optional[str] = Query(None, description="Filter by protection (none, required, active)"),
    case_id: Optional[int] = Query(None, description="Filter by case ID"),
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all witnesses with optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **status**: Filter witnesses by status
    - **protection**: Filter witnesses by protection level
    - **case_id**: Filter witnesses by case
    """
    return witness_service.get_witnesses(db, skip, limit, status, protection, case_id)

@router.get("/{witness_id}", response_model=witness_schema.WitnessResponse)
def get_witness(
    witness_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific witness by ID.
    """
    return witness_service.get_witness(db, witness_id)

@router.put("/{witness_id}", response_model=witness_schema.WitnessResponse)
def update_witness(
    witness_id: int,
    witness_update: witness_schema.WitnessUpdate,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a witness.
    
    You can update any of the following fields:
    - **name**
    - **contact**
    - **statement_date**
    - **status**
    - **protection**
    - **case_id**
    - **is_anonymous**
    """
    return witness_service.update_witness(db, witness_id, witness_update, current_user.id)

@router.delete("/{witness_id}")
def delete_witness(
    witness_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a witness.
    """
    return witness_service.delete_witness(db, witness_id, current_user.id)
