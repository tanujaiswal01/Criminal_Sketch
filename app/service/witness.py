from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from db import models
from schema import witness as witness_schema
from typing import List, Optional

def create_witness(db: Session, witness: witness_schema.WitnessCreate, user_id: int):
    """Create a new witness"""
    new_witness = models.Witness(
        name=witness.name,
        contact=witness.contact,
        statement_date=witness.statement_date,
        status=witness.status,
        protection=witness.protection,
        case_id=witness.case_id,
        is_anonymous=witness.is_anonymous,
        created_by=user_id
    )
    db.add(new_witness)
    db.commit()
    db.refresh(new_witness)
    return new_witness

def get_witness(db: Session, witness_id: int):
    """Get a single witness by ID"""
    witness = db.query(models.Witness).filter(models.Witness.id == witness_id).first()
    if not witness:
        raise HTTPException(status_code=404, detail="Witness not found")
    return witness

def get_witnesses(
    db: Session, 
    skip: int = 0, 
    limit: int = 100, 
    status: Optional[str] = None,
    protection: Optional[str] = None,
    case_id: Optional[int] = None
):
    """Get all witnesses with optional filtering"""
    query = db.query(models.Witness)
    
    if status:
        query = query.filter(models.Witness.status == status)
    if protection:
        query = query.filter(models.Witness.protection == protection)
    if case_id:
        query = query.filter(models.Witness.case_id == case_id)
    
    return query.offset(skip).limit(limit).all()

def update_witness(db: Session, witness_id: int, witness_update: witness_schema.WitnessUpdate, user_id: int):
    """Update a witness"""
    witness = db.query(models.Witness).filter(models.Witness.id == witness_id).first()
    if not witness:
        raise HTTPException(status_code=404, detail="Witness not found")
    
    # Update only provided fields
    update_data = witness_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(witness, field, value)
    
    db.commit()
    db.refresh(witness)
    return witness

def delete_witness(db: Session, witness_id: int, user_id: int):
    """Delete a witness"""
    witness = db.query(models.Witness).filter(models.Witness.id == witness_id).first()
    if not witness:
        raise HTTPException(status_code=404, detail="Witness not found")
    
    db.delete(witness)
    db.commit()
    return {"message": "Witness deleted successfully"}
