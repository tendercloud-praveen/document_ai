from typing import Dict, Any
from pydantic import BaseModel

class UpdateDocumentRequest(BaseModel):
    extracted_data: Dict[str, Any]