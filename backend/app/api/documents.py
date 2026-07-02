# from pathlib import Path

# from fastapi import APIRouter, UploadFile, File, Depends
# from sqlalchemy.orm import Session

# from app.graph.workflow import graph
# from app.database.database import get_db
# from app.repository.document_repository import DocumentRepository

# router = APIRouter(
#     prefix="/documents",
#     tags=["Documents"]
# )

# UPLOAD_DIR = Path("app/uploads")
# UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# @router.post("/upload")
# async def upload_document(
#     file: UploadFile = File(...),
#     db: Session = Depends(get_db)     # ✅ Correct place
# ):
#     file_path = UPLOAD_DIR / file.filename

#     with open(file_path, "wb") as f:
#         f.write(await file.read())

#     result = graph.invoke({
#         "file_path": str(file_path)
#     })

#     repo = DocumentRepository(db)

#     saved_doc = repo.save(result)

#     return {
#         "message": "Document processed and saved successfully",
#         "data": {
#             "id": saved_doc.id,
#             "document_type": saved_doc.document_type
#         }
#     }
from pathlib import Path
from typing import List

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.graph.workflow import graph
from app.database.database import get_db
from app.repository.document_repository import DocumentRepository

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

UPLOAD_DIR = Path("app/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/upload")
async def upload_document(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    repo = DocumentRepository(db)

    summary = {}
    documents = {}

    for file in files:
        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as f:
            f.write(await file.read())

        result = graph.invoke({
            "file_name": file.filename,
            "file_path": str(file_path)
        })

        saved_doc = repo.save(result)

        document_type = result.get("document_type", "Unknown")

        # Count document types
        summary[document_type] = summary.get(document_type, 0) + 1

        # Create list for each type
        if document_type not in documents:
            documents[document_type] = []

        documents[document_type].append({
            "id": saved_doc.id,
            "file_name": file.filename,
            "confidence": result.get("confidence"),
            "summary": result.get("summary"),
            "fields": result.get("extracted_data")
        })

    return {
        "message": f"{len(files)} document(s) processed successfully",
        "summary": summary,
        "documents": documents
    }