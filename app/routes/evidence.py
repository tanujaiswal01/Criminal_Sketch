from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from db import session
from schema import evidence as evidence_schema
from service import evidence as evidence_service
from core.dependencies import get_current_user
from db.models import User
import os

router = APIRouter(
    prefix="/evidence",
    tags=["evidence"]
)

@router.post("/upload", response_model=evidence_schema.EvidenceResponse, status_code=status.HTTP_201_CREATED)
async def upload_evidence(
    file: UploadFile = File(...),
    case_id: Optional[int] = Form(None),
    uploaded_by_name: str = Form(...),
    description: Optional[str] = Form(None),
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload evidence file (photo, video, or document).
    
    - **file**: The file to upload (images, videos, PDFs, etc.)
    - **case_id**: Optional case ID to link evidence to
    - **uploaded_by_name**: Name of uploader (e.g., "Det. Johnson", "CSI Martinez")
    - **description**: Optional description of the evidence
    
    Supported formats:
    - Images: .jpg, .jpeg, .png, .gif, .bmp, .tiff
    - Videos: .mp4, .avi, .mov, .wmv, .flv, .mkv
    - Documents: .pdf, .doc, .docx, .txt, .rtf
    """
    return await evidence_service.upload_evidence(
        db, file, case_id, uploaded_by_name, description, current_user.id
    )

@router.get("/", response_model=List[evidence_schema.EvidenceResponse])
def get_all_evidence(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    case_id: Optional[int] = Query(None, description="Filter by case ID"),
    file_type: Optional[str] = Query(None, description="Filter by file type (image, video, document)"),
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all evidence files with optional filtering.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **case_id**: Filter by case
    - **file_type**: Filter by file type
    """
    evidence_list = evidence_service.get_all_evidence(db, skip, limit, case_id, file_type)
    
    # Add chain records count to each evidence
    result = []
    for evidence in evidence_list:
        chain_count = len(evidence_service.get_chain_of_custody(db, evidence.id))
        evidence_dict = evidence.__dict__
        evidence_dict['chain_records_count'] = chain_count
        result.append(evidence_dict)
    
    return result

@router.get("/{evidence_id}", response_model=evidence_schema.EvidenceWithChain)
def get_evidence_detail(
    evidence_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get evidence details with full chain of custody.
    """
    # Add chain record for access
    evidence_service.add_chain_record(
        db,
        evidence_id,
        "accessed",
        current_user.id,
        current_user.username,
        f"Evidence accessed by {current_user.username}"
    )
    
    return evidence_service.get_evidence_with_chain(db, evidence_id)

@router.get("/{evidence_id}/download")
def download_evidence(
    evidence_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Download evidence file.
    """
    evidence = evidence_service.get_evidence(db, evidence_id)
    
    if not os.path.exists(evidence.file_path):
        raise HTTPException(status_code=404, detail="File not found on server")
    
    # Add chain record for download
    evidence_service.add_chain_record(
        db,
        evidence_id,
        "downloaded",
        current_user.id,
        current_user.username,
        f"Evidence downloaded by {current_user.username}"
    )
    
    return FileResponse(
        path=evidence.file_path,
        filename=evidence.original_filename,
        media_type='application/octet-stream'
    )

@router.get("/{evidence_id}/chain", response_model=List[evidence_schema.ChainOfCustodyResponse])
def get_chain_of_custody(
    evidence_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get chain of custody records for an evidence.
    """
    return evidence_service.get_chain_of_custody(db, evidence_id)

@router.post("/{evidence_id}/chain", response_model=evidence_schema.ChainOfCustodyResponse)
def add_chain_record(
    evidence_id: int,
    action: str = Form(...),
    notes: Optional[str] = Form(None),
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Add a chain of custody record.
    
    - **action**: Action performed (e.g., "transferred", "analyzed", "examined")
    - **notes**: Optional notes about the action
    """
    return evidence_service.add_chain_record(
        db,
        evidence_id,
        action,
        current_user.id,
        current_user.username,
        notes
    )

@router.put("/{evidence_id}", response_model=evidence_schema.EvidenceResponse)
def update_evidence(
    evidence_id: int,
    evidence_update: evidence_schema.EvidenceUpdate,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update evidence metadata.
    
    - **description**: Update description
    - **case_id**: Update case association
    """
    return evidence_service.update_evidence(db, evidence_id, evidence_update, current_user.id, current_user.username)

@router.delete("/{evidence_id}")
def delete_evidence(
    evidence_id: int,
    db: Session = Depends(session.get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete evidence file and all associated records.
    """
    return evidence_service.delete_evidence(db, evidence_id, current_user.id, current_user.username)
