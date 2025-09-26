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
    if "doctor_id" in data and isinstance(data["doctor_id"], str) and ObjectId.is_valid(data["doctor_id"]):
        data["doctor_id"] = ObjectId(data["doctor_id"])
    return data

async def create_patient(data: Dict[str, Any]) -> dict:
    coll = get_collection("patients")
    data = _convert_refs(data)
    data["created_at"] = datetime.utcnow()
    res = await coll.insert_one(data)
    created = await coll.find_one({"_id": res.inserted_id})
    return serialize_doc(created)

async def get_patient_by_id(patient_id: str) -> Optional[dict]:
    coll = get_collection("patients")
    doc = await coll.find_one({"_id": _oid(patient_id)})
    return serialize_doc(doc)

async def list_patients(skip: int = 0, limit: int = 50, doctor_id: Optional[str] = None, q: Optional[str] = None) -> List[dict]:
    coll = get_collection("patients")
    query: Dict[str, Any] = {}
    if doctor_id:
        query["doctor_id"] = _oid(doctor_id)
    if q:
        query["$or"] = [
            {"first_name": {"$regex": q, "$options": "i"}},
            {"last_name":  {"$regex": q, "$options": "i"}},
            {"national_id": {"$regex": q, "$options": "i"}},
        ]
    cursor = coll.find(query, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]

async def update_patient(patient_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("patients")
    data = _convert_refs(data)
    await coll.update_one({"_id": _oid(patient_id)}, {"$set": data})
    return await get_patient_by_id(patient_id)

async def delete_patient(patient_id: str) -> bool:
    coll = get_collection("patients")
    res = await coll.delete_one({"_id": _oid(patient_id)})
    return res.deleted_count == 1
