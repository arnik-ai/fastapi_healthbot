from typing import Optional, List, Dict, Any
from bson import ObjectId
from database import get_collection
from utils.serialize import serialize_doc
from datetime import datetime

def _oid(id: str) -> ObjectId:
    if not ObjectId.is_valid(id):
        raise ValueError("Invalid ObjectId")
    return ObjectId(id)

async def create_file_record(data: Dict[str, Any]) -> dict:
    coll = get_collection("files")
    data["uploaded_at"] = datetime.utcnow()
    res = await coll.insert_one(data)
    created = await coll.find_one({"_id": res.inserted_id})
    return serialize_doc(created)

async def get_file_by_id(file_id: str) -> Optional[dict]:
    coll = get_collection("files")
    doc = await coll.find_one({"_id": _oid(file_id)})
    return serialize_doc(doc)

async def list_files(skip: int = 0, limit: int = 50, patient_id: Optional[str] = None) -> List[dict]:
    coll = get_collection("files")
    query: Dict[str, Any] = {}
    if patient_id:
        query["patient_id"] = _oid(patient_id)
    cursor = coll.find(query, skip=skip, limit=limit).sort("_id", -1)
    return [serialize_doc(d) async for d in cursor]

async def delete_file(file_id: str) -> bool:
    coll = get_collection("files")
    res = await coll.delete_one({"_id": _oid(file_id)})
    return res.deleted_count == 1
