from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class HealthMetricsCreate(BaseModel):
    patient_id: str  # ObjectId as str
    temperature: float = Field(..., ge=30, le=45)
    humidity: int = Field(..., ge=0, le=100)
    breathing: int = Field(..., ge=0, le=60)
    oxygen: int = Field(..., ge=50, le=100)
    fever: Optional[bool] = None  # اگر None باشد از روی دما محاسبه می‌کنیم

class HealthMetricsUpdate(BaseModel):
    temperature: Optional[float] = Field(default=None, ge=30, le=45)
    humidity: Optional[int] = Field(default=None, ge=0, le=100)
    breathing: Optional[int] = Field(default=None, ge=0, le=60)
    oxygen: Optional[int] = Field(default=None, ge=50, le=100)
    fever: Optional[bool] = None

class HealthMetricsResponse(HealthMetricsCreate):
    id: str
    created_at: datetime
