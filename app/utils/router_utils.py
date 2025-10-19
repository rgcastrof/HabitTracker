from app.utils.zip_utils import generate_zip_stream
from fastapi.responses import StreamingResponse
from fastapi import APIRouter
from app.database.mini_db import MiniDb

# Funcionalidade 5
router = APIRouter(prefix="/export", tags=["export"])

db_users = MiniDb(
        filename="users.csv",
        fields=["id", "name", "email", "passwd", "register_date", "deleted", "active"]
    )

db_habits = MiniDb(
        filename="habits.csv",
        fields=["id", "user_id", "name", "description", "frequence", "creation_date", "deleted"]
    )

@router.get("/csv.zip")
async def export_csvs_zip():
    data_sources = {
        "users": db_users.read(),
        "habits": db_habits.read()
    }
    return StreamingResponse(
        generate_zip_stream(data_sources),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=csvs.zip"}
    )
