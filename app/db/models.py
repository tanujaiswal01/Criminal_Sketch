from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from db.session import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String, default="user")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    case_name = Column(String, index=True)
    case_details = Column(String)
    investigator = Column(String)
    status = Column(String, default="active")
    priority = Column(String, default="normal")  # low, normal, high, urgent
    review_due_date = Column(DateTime(timezone=True), nullable=True)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    assigned_to = Column(Integer, ForeignKey("users.id"), index=True, nullable=True)  # Investigator user ID
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    witnesses = relationship("Witness", back_populates="case", cascade="all, delete-orphan")
    evidence_items = relationship("Evidence", back_populates="case", cascade="all, delete-orphan")

class Witness(Base):
    __tablename__ = "witnesses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    contact = Column(String)  # Email or phone
    statement_date = Column(DateTime(timezone=True))
    status = Column(String, default="pending")  # pending, interviewed, follow-up
    protection = Column(String, default="none")  # none, required, active
    case_id = Column(Integer, ForeignKey("cases.id"), index=True)
    is_anonymous = Column(Boolean, default=False)
    created_by = Column(Integer, ForeignKey("users.id"), index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="witnesses")

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    original_filename = Column(String)
    file_path = Column(String)
    file_type = Column(String)  # image, video, document, etc.
    file_size = Column(Integer)  # in bytes
    case_id = Column(Integer, ForeignKey("cases.id"), index=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"), index=True)
    uploaded_by_name = Column(String)  # e.g., "Det. Johnson"
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    case = relationship("Case", back_populates="evidence_items")
    chain_records = relationship("ChainOfCustody", back_populates="evidence", cascade="all, delete-orphan")

class ChainOfCustody(Base):
    __tablename__ = "chain_of_custody"

    id = Column(Integer, primary_key=True, index=True)
    evidence_id = Column(Integer, ForeignKey("evidence.id"), index=True)
    action = Column(String)  # uploaded, accessed, transferred, analyzed, etc.
    performed_by = Column(Integer, ForeignKey("users.id"), index=True)
    performed_by_name = Column(String)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    evidence = relationship("Evidence", back_populates="chain_records")
