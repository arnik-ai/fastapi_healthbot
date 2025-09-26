from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from models.patient import PatientCreate, PatientUpdate
from crud.patient import (
    create_patient, get_patient_by_id, list_patients,
    update_patient, delete_patient
)

router = APIRouter()

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_patient(payload: PatientCreate):
    if payload.doctor_id:
        _check_oid(payload.doctor_id)
    return await create_patient(payload.model_dump())

@router.get("/")
async def get_patients(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    doctor_id: Optional[str] = None,
    q: Optional[str] = None
):
    if doctor_id:
        _check_oid(doctor_id)
    return await list_patients(skip=skip, limit=limit, doctor_id=doctor_id, q=q)

@router.get("/{patient_id}")
async def get_patient(patient_id: str):
    _check_oid(patient_id)
    found = await get_patient_by_id(patient_id)
    if not found:
        raise HTTPException(404, "Patient not found")
    return found

@router.patch("/{patient_id}")
async def patch_patient(patient_id: str, payload: PatientUpdate):
    _check_oid(patient_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    if "doctor_id" in data and data["doctor_id"]:
        _check_oid(data["doctor_id"])
    updated = await update_patient(patient_id, data)
    if not updated:
        raise HTTPException(404, "Patient not found")
    return updated

@router.delete("/{patient_id}", status_code=204)
async def remove_patient(patient_id: str):
    _check_oid(patient_id)
    ok = await delete_patient(patient_id)
    if not ok:
        raise HTTPException(404, "Patient not found")
