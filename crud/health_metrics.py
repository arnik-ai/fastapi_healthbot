from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc
from datetime import datetime

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

def _convert_refs(data: Dict[str, Any]) -> Dict[str, Any]:
    if "patient_id" in data and isinstance(data["patient_id"], str) and ObjectId.is_valid(data["patient_id"]):
        data["patient_id"] = ObjectId(data["patient_id"])
    return data

def _compute_fever(data: Dict[str, Any]) -> None:
    if data.get("fever") is None and (temp := data.get("temperature")) is not None:
        try:
            data["fever"] = float(temp) >= 38.0
        except Exception:
            pass

async def create_metrics(data: Dict[str, Any]) -> dict:
    coll = get_collection("health_metrics")
    data = _convert_refs(data)
    _compute_fever(data)
    data["created_at"] = datetime.utcnow()
    res = await coll.insert_one(data)
    created = await coll.find_one({"_id": res.inserted_id})
    return serialize_doc(created)

async def get_metrics_by_id(metrics_id: str) -> Optional[dict]:
    coll = get_collection("health_metrics")
    doc = await coll.find_one({"_id": _oid(metrics_id)})
    return serialize_doc(doc)

async def list_metrics(skip: int = 0, limit: int = 50, patient_id: Optional[str] = None) -> List[dict]:
    coll = get_collection("health_metrics")
    query: Dict[str, Any] = {}
    if patient_id:
        query["patient_id"] = _oid(patient_id)
    cursor = coll.find(query, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]

async def update_metrics(metrics_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("health_metrics")
    data = _convert_refs(data)
    if "fever" not in data and "temperature" in data:
        _compute_fever(data)
    await coll.update_one({"_id": _oid(metrics_id)}, {"$set": data})
    return await get_metrics_by_id(metrics_id)

async def delete_metrics(metrics_id: str) -> bool:
    coll = get_collection("health_metrics")
    res = await coll.delete_one({"_id": _oid(metrics_id)})
    return res.deleted_count == 1
