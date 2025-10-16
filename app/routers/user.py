from fastapi import APIRouter, Query, HTTPException
from app.database.mini_db import MiniDb
from app.models import User, CountResponse
from datetime import datetime
from pydantic import BaseModel
from typing import List

class UsersPaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int
    users: List[User]

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

@router.get("/", response_model=UsersPaginationResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1)):
    all_users = db.read()
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = [User(**u) for u in all_users[start:end]]
    total = len(all_users)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "users": paginated_users
    }

# TODO: Fazer o CRUD completo da entidade

@router.get("/count", response_model=CountResponse)
async def get_count():
    try:
        all_users = db.read()
        total = len(all_users)
        return {"total_entities": total}
    except Exception as e:
        print(f"Erro ao ler banco de dados: {e}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível acessar ou ler banco de dados"
        )
