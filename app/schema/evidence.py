from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ChainOfCustodyBase(BaseModel):
    action: str
    performed_by_name: str
    notes: Optional[str] = None

class ChainOfCustodyResponse(ChainOfCustodyBase):
    id: int
    evidence_id: int
    performed_by: int
    created_at: datetime

    class Config:
        from_attributes = True

class EvidenceBase(BaseModel):
    original_filename: str
    file_type: str
    case_id: Optional[int] = None
    uploaded_by_name: str
    description: Optional[str] = None

class EvidenceCreate(EvidenceBase):
    pass

class EvidenceUpdate(BaseModel):
    description: Optional[str] = None
    case_id: Optional[int] = None

class EvidenceResponse(EvidenceBase):
    id: int
    filename: str
    file_path: str
    file_size: int
    uploaded_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    chain_records_count: Optional[int] = 0

    class Config:
        from_attributes = True

class EvidenceWithChain(EvidenceResponse):
    chain_of_custody: List[ChainOfCustodyResponse] = []

    class Config:
        from_attributes = True
