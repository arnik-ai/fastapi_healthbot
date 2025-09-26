from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from bson import ObjectId
from models.health_metrics import HealthMetricsCreate, HealthMetricsUpdate
from crud.health_metrics import (
    create_metrics, get_metrics_by_id, list_metrics,
    update_metrics, delete_metrics
)

router = APIRouter()

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

@router.post("/", status_code=201)
async def add_metrics(payload: HealthMetricsCreate):
    _check_oid(payload.patient_id)
    return await create_metrics(payload.model_dump())

@router.get("/")
async def get_metrics(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: Optional[str] = None
):
    if patient_id:
        _check_oid(patient_id)
    return await list_metrics(skip=skip, limit=limit, patient_id=patient_id)

@router.get("/{metrics_id}")
async def get_metrics_item(metrics_id: str):
    _check_oid(metrics_id)
    found = await get_metrics_by_id(metrics_id)
    if not found:
        raise HTTPException(404, "Metrics not found")
    return found

@router.patch("/{metrics_id}")
async def patch_metrics(metrics_id: str, payload: HealthMetricsUpdate):
    _check_oid(metrics_id)
    data = {k: v for k, v in payload.model_dump().items() if v is not None}
    updated = await update_metrics(metrics_id, data)
    if not updated:
        raise HTTPException(404, "Metrics not found")
    return updated

@router.delete("/{metrics_id}", status_code=204)
async def remove_metrics(metrics_id: str):
    _check_oid(metrics_id)
    ok = await delete_metrics(metrics_id)
    if not ok:
        raise HTTPException(404, "Metrics not found")
