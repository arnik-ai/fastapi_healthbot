from typing import Dict, Any, List, Optional
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

async def get_full_record(patient_id: str, limit_metrics: int = 20) -> Dict[str, Any] | None:
    patients = get_collection("patients")
    doctors  = get_collection("doctors")
    metrics  = get_collection("health_metrics")
    files    = get_collection("files")

    p = await patients.find_one({"_id": _oid(patient_id)})
    if not p:
        return None

    d = None
    if p.get("doctor_id"):
        d = await doctors.find_one({"_id": p["doctor_id"]})

    ms: List[Dict[str, Any]] = [
        serialize_doc(m)
        async for m in metrics.find({"patient_id": _oid(patient_id)}).sort("_id", -1).limit(limit_metrics)
    ]
    latest = ms[0] if ms else None

    fs: List[Dict[str, Any]] = [
        serialize_doc(f)
        async for f in files.find({"patient_id": _oid(patient_id)}).sort("_id", -1)
    ]

    return {
        "patient": serialize_doc(p),
        "doctor": serialize_doc(d) if d else None,
        "latest_metrics": latest,
        "metrics": ms,
        "files": fs,
    }
