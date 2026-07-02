from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

from app.database.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    file_name = Column(String)
    file_path = Column(String)

    raw_text = Column(Text)

    document_type = Column(String)
    confidence = Column(Float)

    summary = Column(Text)
    extracted_data = Column(JSON)

    # Pending / Approved / Rejected
    status = Column(String, default="Pending")

    # System / Human
    approved_by = Column(String, nullable=True)

    approved_date = Column(DateTime, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

    updated_at = Column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now()
    )