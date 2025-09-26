from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    specialty: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class DoctorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    specialty: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class DoctorResponse(DoctorCreate):
    id: str
    created_at: datetime
