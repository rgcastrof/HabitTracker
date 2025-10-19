from app.models.user import *
from app.models.hash import *
from app.utils.pagination import paginate_data
from fastapi import APIRouter, Query, HTTPException
from datetime import datetime
from app.routers.utils import db_users

router = APIRouter(prefix="/users", tags=["Users"])

# Cria usuario
@router.post("/", response_model=User, status_code=201)
async def create_user(user: UserCreate):
    user_data = user.model_dump()
    user_data["register_date"] = datetime.now()
    created_user_data = db_users.insert(user_data)

    if not created_user_data:
        raise HTTPException(detail="Failed to create user", status_code=500)
    return User(**created_user_data)

# Read de um usuario inidividual
@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    searched_user = db_users.read_one(user_id)
    if not searched_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User.model_validate(searched_user)

# Update
@router.put("/{user_id}", response_model=UserUpdate)
async def update_user(user_id: int, user: UserUpdate):
    user_update_data = user.model_dump()

    updated_data = db_users.update(user_id, user_update_data)

    if not updated_data:
        raise HTTPException(status_code=404, detail="User with id {user_id} not found")
    return UserUpdate.model_validate(updated_data)

# Delete
@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    success = db_users.delete(user_id);
    if not success:
        raise HTTPException(status_code=404, detail=f"User with id: {user_id} not found.")
    db_users.vacuum()
    return

# Retorna página
@router.get("/", response_model=UsersPaginationResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1)):
    all_users = db_users.read()
    return paginate_data(all_users, page, page_size, User)
