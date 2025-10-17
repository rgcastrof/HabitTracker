from app.models.user import *
from fastapi import APIRouter, Query, HTTPException
from app.database.mini_db import MiniDb
from datetime import datetime

router = APIRouter(prefix="/users", tags=["Users"])

db = MiniDb(
        filename="users.csv",
        fields=["id", "name", "email", "passwd", "register_date", "deleted", "active"]
    )

# Cria usuario
@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    user_data = user.model_dump()
    user_data["register_date"] = datetime.now()
    created_user_data = db.insert(user_data)

    if not created_user_data:
        raise HTTPException(detail="Failed to create user", status_code=500)
    return User.model_validate(created_user_data)

# Retorna página
@router.get("/", response_model=UsersPaginationResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1)):
    all_users = db.read()
    start = (page - 1) * page_size
    end = start + page_size
    paginated_users = [User.model_validate(u) for u in all_users[start:end]]
    total = len(all_users)

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "users": paginated_users
    }

# TODO: Fazer o CRUD completo da entidade

@router.get("/count", response_model=UsersCountResponse)
async def get_count():
    try:
        all_users = db.read()
        total = len(all_users)
        return {"total_users": total}
    except Exception as e:
        print(f"Erro ao ler banco de dados: {e}")
        raise HTTPException(
            status_code=500,
            detail="Não foi possível acessar ou ler banco de dados"
        )
