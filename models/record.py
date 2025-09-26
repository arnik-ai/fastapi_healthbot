from pydantic import BaseModel
from typing import List, Optional, Any

class PatientRecordResponse(BaseModel):
    patient: Any
    doctor: Optional[Any] = None
    latest_metrics: Optional[Any] = None
    metrics: List[Any] = []
    files: List[Any] = []
