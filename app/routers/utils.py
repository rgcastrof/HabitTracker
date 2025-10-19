from pydantic import BaseModel
from app.utils.zip_utils import generate_zip_stream
from app.models.hash import HashRequest, HashResponse
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, HTTPException
from app.database.mini_db import MiniDb
import hashlib

router = APIRouter(prefix="/utils", tags=["Utils"])

db_users = MiniDb(
        filename="users.csv",
        fields=["id", "name", "email", "passwd", "register_date", "deleted", "active"]
    )

db_habits = MiniDb(
        filename="habits.csv",
        fields=["id", "user_id", "name", "description", "frequence", "creation_date", "deleted"]
    )

data_sources = {
    "users": db_users.read(),
    "habits": db_habits.read()
}

class Count(BaseModel):
    total_entities: int

@router.get("/count", response_model=Count)
async def count():
    total = sum(len(data_list) for data_list in data_sources.values())
    return {"total_entities": total}

# Funcionalidade 5
@router.get("/export")
async def export_csvs_zip():
    return StreamingResponse(
        generate_zip_stream(data_sources),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=csvs.zip"}
    )

# Funcionalidade 6
@router.post("/hash", response_model=HashResponse)
async def generate_hash(req: HashRequest):
    hash_func = req.hash_func.lower()
    if hash_func not in ("md5", "sha1", "sha256"):
        raise HTTPException(status_code=400, detail="A função de hash deve ser md5, sha1, ou sha256")
    h = hashlib.new(hash_func)
    h.update(req.data.encode())
    return HashResponse(hash=h.hexdigest())
