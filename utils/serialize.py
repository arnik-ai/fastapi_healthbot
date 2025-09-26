from typing import Any, Dict
from bson import ObjectId

def to_str_id(value: Any) -> Any:
    if isinstance(value, ObjectId):
        return str(value)
    if isinstance(value, list):
        return [to_str_id(v) for v in value]
    if isinstance(value, dict):
        return {k: to_str_id(v) for k, v in value.items()}
    return value

def serialize_doc(doc: Dict[str, Any]) -> Dict[str, Any] | None:
    if not doc:
        return None
    doc = dict(doc)
    if "_id" in doc:
        doc["id"] = str(doc.pop("_id"))
    return to_str_id(doc)
