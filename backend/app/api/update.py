from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.models.documet import Document
from app.schema.updates import UpdateDocumentRequest

router = APIRouter(
    prefix="/approval",
    tags=["Human Verification"]
)


@router.put("/update/{document_id}")
def update_document(
    document_id: int,
    request: UpdateDocumentRequest,
    db: Session = Depends(get_db)
):
    document = (
        db.query(Document)
        .filter(Document.id == document_id)
        .first()
    )

    if document is None:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    # document.document_type = request.document_type
    # document.summary = request.summary
    # document.confidence = request.confidence

    document.extracted_data = request.extracted_data

    document.status = "Pending"

    db.commit()
    db.refresh(document)

    return {
        "message": "Document updated successfully",
        "document": document
    }