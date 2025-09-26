from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from crud.record import get_full_record

router = APIRouter()

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.get("/{patient_id}")
async def get_patient_record(patient_id: str, limit_metrics: int = Query(20, ge=1, le=200)):
    _check_oid(patient_id)
    rec = await get_full_record(patient_id, limit_metrics=limit_metrics)
    if not rec:
        raise HTTPException(404, "Patient not found")
    return rec
