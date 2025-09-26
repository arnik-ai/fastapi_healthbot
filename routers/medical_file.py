from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from starlette.responses import FileResponse
from typing import Optional
from bson import ObjectId
import os

from crud.medical_file import create_file_record, get_file_by_id, list_files, delete_file

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter()

def _check_oid(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Invalid id")

def _safe_join(base: str, *paths: str) -> str:
    base_abs = os.path.abspath(base)
    full = os.path.abspath(os.path.join(base_abs, *paths))
    if not full.startswith(base_abs):
        raise HTTPException(400, "Invalid path")
    return full

@router.post("/upload", status_code=201)
async def upload_file(
    patient_id: str = Form(...),
    file: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    _check_oid(patient_id)
    filename = file.filename
    dest_path = _safe_join(UPLOAD_DIR, filename)

    with open(dest_path, "wb") as f:
        content = await file.read()
        f.write(content)

    data = {
        "patient_id": ObjectId(patient_id),
        "filename": filename,
        "path": dest_path,
        "content_type": file.content_type,
        "size": os.path.getsize(dest_path),
        "description": description,
    }
    return await create_file_record(data)

@router.get("/")
async def get_files(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    patient_id: Optional[str] = None
):
    if patient_id:
        _check_oid(patient_id)
    return await list_files(skip=skip, limit=limit, patient_id=patient_id)

@router.get("/{file_id}/download")
async def download_file(
    file_id: str,
    disposition: str = Query("inline", pattern=r"^(inline|attachment)$")
):
    _check_oid(file_id)
    rec = await get_file_by_id(file_id)
    if not rec:
        raise HTTPException(404, "File not found")
    path = rec["path"]
    if not os.path.isfile(path):
        raise HTTPException(410, "File missing on server")
    return FileResponse(
        path,
        media_type=rec.get("content_type") or "application/octet-stream",
        filename=rec["filename"]
    )

@router.delete("/{file_id}", status_code=204)
async def remove_file(file_id: str):
    _check_oid(file_id)
    rec = await get_file_by_id(file_id)
    if not rec:
        raise HTTPException(404, "File not found")
    try:
        if os.path.isfile(rec["path"]):
            os.remove(rec["path"])
    except Exception:
        pass
    ok = await delete_file(file_id)
    if not ok:
        raise HTTPException(404, "File not found in DB")
