from typing import TypedDict

class DocumentState(TypedDict):
    file_name: str
    file_path: str
    raw_text: str
    document_type: str
    confidence: float
    summary: str
    extracted_data: dict
    status: str
    approved_by: str
    approved_date: object