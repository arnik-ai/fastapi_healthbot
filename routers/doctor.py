from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from models.doctor import DoctorCreate, DoctorUpdate
from crud.doctor import (
    create_doctor, get_doctor_by_id, list_doctors,
    update_doctor, delete_doctor
)

router = APIRouter()

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_doctor(payload: DoctorCreate):
    return await create_doctor(payload.model_dump())

@router.get("/")
async def get_doctors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    q: Optional[str] = None
):
    return await list_doctors(skip=skip, limit=limit, q=q)

@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str):
    _check_oid(doctor_id)
    found = await get_doctor_by_id(doctor_id)
    if not found:
        raise HTTPException(404, "Doctor not found")
    return found

@router.patch("/{doctor_id}")
async def patch_doctor(doctor_id: str, payload: DoctorUpdate):
    _check_oid(doctor_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await update_doctor(doctor_id, data)
    if not updated:
        raise HTTPException(404, "Doctor not found")
    return updated

@router.delete("/{doctor_id}", status_code=204)
async def remove_doctor(doctor_id: str):
    _check_oid(doctor_id)
    ok = await delete_doctor(doctor_id)
    if not ok:
        raise HTTPException(404, "Doctor not found")
