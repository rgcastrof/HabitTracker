from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from app.models.habit import Habit
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from app.schemas.habit import HabitRead
from sqlmodel import Session, select
from app.core.database import get_session
from app.crud.base import CRUDBase

router = APIRouter()
crud_user = CRUDBase(User)

# CRUD Operations
# Create
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_session)):
    created_user = crud_user.create(user, db)
    if not created_user:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")
    return created_user

# Read (all)
@router.get("/", response_model=list[UserRead])
def get_all_users(
    offset=Query(default=0),
    limit=Query(default=10),
    db: Session = Depends(get_session)
):
    return crud_user.get_all(offset=offset, limit=limit, db=db)

# Read (one)
@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_session)):
    getted_user = crud_user.get_by_id(user_id, db)
    if not getted_user:
        raise HTTPException(status_code=404, detail=f"Usuário com id: {user_id} não encontrado")
    return getted_user

# Update
@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    updated_user = crud_user.update(user_id, user_update, db)
    if not updated_user:
        raise HTTPException(status_code=500, detail="Erro ao atualizar dados do usuário no banco")
    return updated_user

# Delete
@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_session)):
    deleted_user = crud_user.delete(user_id, db)
    if not deleted_user:
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário")


#  Consultas complexas
@router.get("/{user_id}/habits", response_model=list[HabitRead])
def get_habits_by_user(
    user_id: int,
    offset: int = Query(default=0),
    limit: int = Query(default=10),
    db: Session = Depends(get_session)
):
    try:
        stmt = select(Habit).join(User).where(User.id == user_id).offset(offset).limit(limit)
        return db.exec(stmt).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar habitos associados a usuario com id {user_id}: {e}"
        )
