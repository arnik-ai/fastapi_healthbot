from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PatientCreate(BaseModel):
    first_name: str
    last_name: str
    national_id: str = Field(..., min_length=10, max_length=10)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[str] = Field(default=None, pattern=r"^(مرد|زن)$")
    gps: Optional[str] = None
    history: Optional[str] = None
    drugs: Optional[str] = None
    allergies: Optional[str] = None
    doctor_id: Optional[str] = None  # مرجع به Doctor (ObjectId as str)
    doctor_name: Optional[str] = None
    image: Optional[str] = None


class PatientUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    national_id: Optional[str] = Field(default=None, min_length=10, max_length=10)
    age: Optional[int] = Field(default=None, ge=0, le=120)
    gender: Optional[str] = Field(default=None, pattern=r"^(مرد|زن)$")
    gps: Optional[str] = None
    history: Optional[str] = None
    drugs: Optional[str] = None
    allergies: Optional[str] = None
    doctor_id: Optional[str] = None
    doctor_name: Optional[str] = None
    image: Optional[str] = None


class PatientResponse(PatientCreate):
    id: str
    created_at: datetime
