from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from db import models
from schema import evidence as evidence_schema
from typing import List, Optional
import os
import uuid
from datetime import datetime

# Evidence storage directory
EVIDENCE_DIR = "static/evidence"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {
    'image': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'],
    'video': ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv'],
    'document': ['.pdf', '.doc', '.docx', '.txt', '.rtf']
}

def get_file_type(filename: str) -> str:
    """Determine file type based on extension"""
    ext = os.path.splitext(filename)[1].lower()
    for file_type, extensions in ALLOWED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return 'other'

def create_chain_record(db: Session, evidence_id: int, action: str, user_id: int, user_name: str, notes: Optional[str] = None):
    """Create a chain of custody record"""
    chain_record = models.ChainOfCustody(
        evidence_id=evidence_id,
        action=action,
        performed_by=user_id,
        performed_by_name=user_name,
        notes=notes
    )
    db.add(chain_record)
    db.commit()
    return chain_record

async def upload_evidence(
    db: Session,
    file: UploadFile,
    case_id: Optional[int],
    uploaded_by_name: str,
    description: Optional[str],
    user_id: int
):
    """Upload evidence file"""
    # Generate unique filename
    file_ext = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = os.path.join(EVIDENCE_DIR, unique_filename)
    
    # Save file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    file_size = len(contents)
    file_type = get_file_type(file.filename)
    
    # Create evidence record
    evidence = models.Evidence(
        filename=unique_filename,
        original_filename=file.filename,
        file_path=file_path,
        file_type=file_type,
        file_size=file_size,
        case_id=case_id,
        uploaded_by=user_id,
        uploaded_by_name=uploaded_by_name,
        description=description
    )
    db.add(evidence)
    db.commit()
    db.refresh(evidence)
    
    # Create initial chain of custody record
    create_chain_record(
        db, 
        evidence.id, 
        "uploaded", 
        user_id, 
        uploaded_by_name,
        f"File uploaded: {file.filename}"
    )
    
    return evidence

def get_evidence(db: Session, evidence_id: int):
    """Get single evidence by ID"""
    evidence = db.query(models.Evidence).filter(models.Evidence.id == evidence_id).first()
    if not evidence:
        raise HTTPException(status_code=404, detail="Evidence not found")
    return evidence

def get_all_evidence(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    case_id: Optional[int] = None,
    file_type: Optional[str] = None
):
    """Get all evidence with optional filtering"""
    query = db.query(models.Evidence)
    
    if case_id:
        query = query.filter(models.Evidence.case_id == case_id)
    if file_type:
        query = query.filter(models.Evidence.file_type == file_type)
    
    return query.offset(skip).limit(limit).all()

def get_evidence_with_chain(db: Session, evidence_id: int):
    """Get evidence with chain of custody records"""
    evidence = get_evidence(db, evidence_id)
    chain_records = db.query(models.ChainOfCustody).filter(
        models.ChainOfCustody.evidence_id == evidence_id
    ).order_by(models.ChainOfCustody.created_at.desc()).all()
    
    return {
        **evidence.__dict__,
        "chain_of_custody": chain_records,
        "chain_records_count": len(chain_records)
    }

def get_chain_of_custody(db: Session, evidence_id: int):
    """Get chain of custody for an evidence"""
    evidence = get_evidence(db, evidence_id)
    return db.query(models.ChainOfCustody).filter(
        models.ChainOfCustody.evidence_id == evidence_id
    ).order_by(models.ChainOfCustody.created_at.desc()).all()

def add_chain_record(
    db: Session,
    evidence_id: int,
    action: str,
    user_id: int,
    user_name: str,
    notes: Optional[str] = None
):
    """Add a chain of custody record"""
    evidence = get_evidence(db, evidence_id)
    return create_chain_record(db, evidence_id, action, user_id, user_name, notes)

def update_evidence(db: Session, evidence_id: int, evidence_update: evidence_schema.EvidenceUpdate, user_id: int, user_name: str):
    """Update evidence metadata"""
    evidence = get_evidence(db, evidence_id)
    
    update_data = evidence_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(evidence, field, value)
    
    db.commit()
    db.refresh(evidence)
    
    # Add chain record for update
    create_chain_record(
        db,
        evidence_id,
        "updated",
        user_id,
        user_name,
        f"Evidence metadata updated"
    )
    
    return evidence

def delete_evidence(db: Session, evidence_id: int, user_id: int, user_name: str):
    """Delete evidence"""
    evidence = get_evidence(db, evidence_id)
    
    # Delete physical file
    if os.path.exists(evidence.file_path):
        os.remove(evidence.file_path)
    
    # Delete chain records
    db.query(models.ChainOfCustody).filter(models.ChainOfCustody.evidence_id == evidence_id).delete()
    
    # Delete evidence record
    db.delete(evidence)
    db.commit()
    
    return {"message": "Evidence deleted successfully"}
