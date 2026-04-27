from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import models
from schema import case as case_schema
from typing import List, Optional

def create_case(db: Session, case: case_schema.CaseCreate, user_id: int):
    """Create a new case"""
    new_case = models.Case(
        case_name=case.case_name,
        case_details=case.case_details,
        investigator=case.investigator,
        status=case.status,
        priority=case.priority,
        review_due_date=case.review_due_date,
        assigned_to=case.assigned_to,
        created_by=user_id
    )
    db.add(new_case)
    db.commit()
    db.refresh(new_case)
    return new_case

def get_case(db: Session, case_id: int):
    """Get a single case by ID"""
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

def get_cases(db: Session, user: models.User, skip: int = 0, limit: int = 100, status: Optional[str] = None):
    """
    Get cases based on user role:
    - Officers: See all cases
    - Investigators: See only cases assigned to them
    - Users: See only cases they created
    """
    query = db.query(models.Case)
    
    # Role-based filtering
    if user.role == "officer":
        # Officers see all cases
        pass
    elif user.role == "investigator":
        # Investigators see only cases assigned to them
        query = query.filter(models.Case.assigned_to == user.id)
    else:
        # Regular users see only cases they created
        query = query.filter(models.Case.created_by == user.id)
    
    # Additional status filtering
    if status:
        query = query.filter(models.Case.status == status)
    
    return query.offset(skip).limit(limit).all()

def update_case(db: Session, case_id: int, case_update: case_schema.CaseUpdate, user_id: int):
    """Update a case"""
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    # Update only provided fields
    update_data = case_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(case, field, value)
    
    db.commit()
    db.refresh(case)
    return case

def delete_case(db: Session, case_id: int, user_id: int):
    """Delete a case"""
    case = db.query(models.Case).filter(models.Case.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    db.delete(case)
    db.commit()
    return {"message": "Case deleted successfully"}
