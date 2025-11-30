from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlmodel import Session, column, select
from app.core.database import get_session
from app.models.habit import Habit
from app.models.record import Record
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.crud.base import logger
from app.schemas.record import RecordRead

from app.crud.base import CRUDBase

router = APIRouter()
crud_habit = CRUDBase(Habit)

@router.post("/", response_model=HabitRead)
def create_habit(user_id: int, habit: HabitCreate, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail=f"Usuário com id: {user_id} não encontrado")
    try:
        db_habit = Habit(**habit.model_dump(), user_id=user_id)
        db.add(db_habit)
        db.commit()
        db.refresh(db_habit)
        return db_habit
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Erro ao criar hábito: {e}")
        raise HTTPException(status_code=500, detail=f"Erro ao criar hábito: {e}")

@router.get("/", response_model=list[HabitRead])
def get_all_habits(
    offset = Query(default=0),
    limit = Query(default=10),
    db: Session = Depends(get_session)
):
    return crud_habit.get_all(offset=offset, limit=limit, db=db)

@router.get("/search", response_model=list[HabitRead])
def get_habit_by_text(
    q: str = "",
    offset: int = Query(default=0),
    limit: int = Query(default=10),
    db: Session = Depends(get_session),
    ):
    try:
        if q:
            stmt = select(Habit).where(func.lower(Habit.name).like(f"%{q.lower()}%"))
        else:
            stmt = select(Habit)
        stmt = stmt.offset(offset).limit(limit)
        return db.exec(stmt).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Consulta nao encontrada: {e}"
        )

@router.get("/{habit_id}", response_model=HabitRead)
def get_habit(habit_id: int, db: Session = Depends(get_session)):
    getted_habit = crud_habit.get_by_id(habit_id, db)
    if not getted_habit:
        raise HTTPException(status_code=404, detail=f"Hábito com id: {habit_id} não encontrado")
    return getted_habit

@router.patch("/{habit_id}", response_model=HabitRead)
def update_habit(habit_id: int, habit_update: HabitUpdate, db: Session = Depends(get_session)):
    updated_habit = crud_habit.update(habit_id, habit_update, db)
    if not updated_habit:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar dados do hábito no banco")
    return updated_habit

@router.delete("/{habit_id}", status_code=204)
def delete_habit(habit_id: int, db: Session = Depends(get_session)):
    deleted_habit = crud_habit.delete(habit_id, db)
    if not deleted_habit:
        raise HTTPException(status_code=500, detail="Erro ao deletar hábito")

@router.get("/{habit_id}/records", response_model=list[RecordRead])
def get_records_by_habit(
    habit_id: int,
    offset: int = Query(default=0),
    limit: int = Query(default=10),
    db: Session = Depends(get_session)
):
    try:
        stmt = select(Record).join(Habit).where(Habit.id == habit_id).order_by(column("creation_date").desc())
        stmt = stmt.offset(offset).limit(limit)
        return db.exec(stmt).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao buscar registros associados a habito com id {habit_id}: {e}"
        )
