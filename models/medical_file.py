from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalFileResponse(BaseModel):
    id: str
    patient_id: str
    filename: str
    path: str
    content_type: Optional[str] = None
    size: Optional[int] = None
    description: Optional[str] = None
    uploaded_at: datetime
