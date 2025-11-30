from datetime import date, datetime, time
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_session
from app.crud.base import CRUDBase
from app.models.habit import Habit
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate
from app.crud.base import logger
from sqlmodel import Session, select
from fastapi import Depends

router =APIRouter()
crud_record = CRUDBase(Record)

@router.post("/", response_model=RecordRead)
def create_record(habit_id: int, record: RecordCreate, db: Session = Depends(get_session)):
    db_habit = db.get(Habit, habit_id)
    if not db_habit:
        raise HTTPException(status_code=404, detail=f"Hábito com id: {habit_id} não encontrado")
    try:
        db_record = Record(**record.model_dump(), habit_id=habit_id)
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except SQLAlchemyError as e:
        db.rollback()
        fmt = f"Erro ao criar registro: {e}"
        logger.error(fmt)
        raise HTTPException(status_code=500, detail=fmt)

@router.get("/", response_model=list[RecordRead])
def get_all_records(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_session)
):
    return crud_record.get_all(offset, limit, db)

# Consulta Complexa: Filtra registros por data
@router.get("/filter-date", response_model=list[RecordRead])
def get_record_by_date(
    user_id: int,
    habit_id: int,
    start_date: date,
    end_date: date,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_session)
):
    try:
        stmt = select(Record).join(Habit).where(Habit.user_id == user_id)
        stmt = stmt.where(Record.habit_id == habit_id)

        start_datetime = datetime.combine(start_date, time.min)
        stmt = stmt.where(Record.creation_date >= start_datetime)

        end_datetime = datetime.combine(end_date, time.max)
        stmt = stmt.where(Record.creation_date <= end_datetime)
        stmt = stmt.offset(offset).limit(limit)

        return db.exec(stmt).all()
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=404,
            detail=f"Não foram encontrados registros durante o intervalo informado: {e}"
        )

@router.get("/{record_id}", response_model=RecordRead)
def get_record(record_id: int, db: Session = Depends(get_session)):
    getted_record = crud_record.get_by_id(record_id, db)
    if not getted_record:
        raise HTTPException(status_code=404, detail=f"Registro com id: {record_id} não encotrado")
    return getted_record

@router.patch("/{record_id}", response_model=RecordRead)
def update_record(record_id: int, record_update: RecordUpdate, db: Session = Depends(get_session)):
    updated_record = crud_record.update(record_id, record_update, db)
    if not updated_record:
        raise HTTPException(status_code=500, detail="Erro ao atualizar dados de registro")
    return updated_record

@router.delete("/{record_id}", status_code=204)
def delete_record(record_id: int, db: Session = Depends(get_session)):
    deleted_record = crud_record.delete(record_id, db)
    if not deleted_record:
        raise HTTPException(status_code=500, detail="Erro ao deletar registro")
