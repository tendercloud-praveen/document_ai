# repositories/document_repository.py

from app.models.documet import Document
from app.database.database import Base  

class DocumentRepository:

    def __init__(self, db):
        self.db = db

    def save(self, state):
        document = Document(
            file_name=state["file_name"],
        file_path=state["file_path"],
    raw_text=state["raw_text"],
    document_type=state["document_type"],
    confidence=state["confidence"],
    summary=state["summary"],
    extracted_data=state["extracted_data"],
    status=state["status"],
    approved_by=state["approved_by"],
    approved_date=state["approved_date"]
        )

        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)

        return document