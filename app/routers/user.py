from app.models.user import *
from app.models.hash import *
from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import StreamingResponse
from app.database.mini_db import MiniDb
from app.utils.zip_utils import generate_zip_stream
from datetime import datetime
import hashlib

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

# Funcionalidade 5
@router.get("/export_zip")
async def export_csv_zip():
    return StreamingResponse(
        generate_zip_stream(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=users.zip"}
    )

# Read de um usuario inidividual
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    searched_user = db.read_one(user_id)
    if not searched_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User.model_validate(searched_user)

# Update
@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    user_update_data = user.model_dump()

    updated_data = db.update(user_id, user_update_data)

    if not updated_data:
        raise HTTPException(status_code=404, detail="User with id {user_id} not found")
    return UserUpdate.model_validate(updated_data)

# Delete
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    success = db.delete(user_id);
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    db.vacuum()
    return

# Conta todas as entidades
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


# Funcionalidade 6
@router.post("/hash", response_model=HashResponse)
async def generate_hash(req: HashRequest):
    hash_func = req.hash_func.lower()
    if hash_func not in ("md5", "sha1", "sha256"):
        raise HTTPException(status_code=400, detail="A função de hash deve ser md5, sha1, ou sha256")
    h = hashlib.new(hash_func)
    h.update(req.data.encode())
    return HashResponse(hash=h.hexdigest())
