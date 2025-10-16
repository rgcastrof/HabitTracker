from fastapi import APIRouter
from app.database.mini_db import MiniDb
from app.models import User
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

db = MiniDb(
        filename="users.csv",
        fields = ["name", "email", "passwd", "register_date", "active"]
    )

@router.post("/", response_model=User)
async def create_user(user: User):
    user_data = user.dict(exclude={"id", "register_date"})
    user_data["register_date"] = datetime.utcnow().isoformat()
    new_id = db.insert(user_data)
    return User(id=new_id, **user_data)
