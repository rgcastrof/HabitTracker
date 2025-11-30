from fastapi import APIRouter, HTTPException, Query
from sqlalchemy.exc import SQLAlchemyError
from app.core.database import get_session
from app.crud.base import CRUDBase
from app.models.habit import Habit
from app.models.record import Record
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate
from app.crud.base import logger
from sqlmodel import Session
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
    offset = Query(default=0),
    limit = Query(default=10),
    db: Session = Depends(get_session)
):
    return crud_record.get_all(offset, limit, db)

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
