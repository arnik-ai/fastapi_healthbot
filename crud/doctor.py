from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc
from datetime import datetime


def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)


async def create_doctor(data: Dict[str, Any]) -> dict:
    coll = get_collection("doctors")
    data["created_at"] = datetime.utcnow()
    res = await coll.insert_one(data)
    created = await coll.find_one({"_id": res.inserted_id})
    return serialize_doc(created)


async def get_doctor_by_id(doctor_id: str) -> Optional[dict]:
    coll = get_collection("doctors")
    doc = await coll.find_one({"_id": _oid(doctor_id)})
    return serialize_doc(doc)


async def list_doctors(skip: int = 0, limit: int = 50, q: Optional[str] = None) -> List[dict]:
    coll = get_collection("doctors")
    query: Dict[str, Any] = {}
    if q:
        query["$or"] = [
            {"first_name": {"$regex": q, "$options": "i"}},
            {"last_name":  {"$regex": q, "$options": "i"}},
            {"specialty":  {"$regex": q, "$options": "i"}},
        ]
    cursor = coll.find(query, skip=skip, limit=limit).sort("_id", 1)
    return [serialize_doc(d) async for d in cursor]


async def update_doctor(doctor_id: str, data: Dict[str, Any]) -> Optional[dict]:
    coll = get_collection("doctors")
    await coll.update_one({"_id": _oid(doctor_id)}, {"$set": data})
    return await get_doctor_by_id(doctor_id)


async def delete_doctor(doctor_id: str) -> bool:
    coll = get_collection("doctors")
    res = await coll.delete_one({"_id": _oid(doctor_id)})
    return res.deleted_count == 1
