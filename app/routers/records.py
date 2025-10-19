from app.models.records import *
from app.utils.pagination import paginate_data
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from app.routers.utils import db_habits, db_records

router = APIRouter(prefix="/records", tags=["Records"])

# Cria registro
@router.post("/", response_model=Record, status_code=201)
async def create_record(record: RecordCreate):
    habits = db_habits.read()

    # Verifica se o habito no id passado existe
    if not any(h['id'] == str(record.habit_id) for h in habits):
        raise HTTPException(status_code=404, detail="Habit not found")

    record_data = record.model_dump()
    record_data["timestamp"] = datetime.now()
    created_record_data = db_records.insert(record_data)

    if not created_record_data:
        raise HTTPException(detail="Failed to create the record", status_code=500)
    return Record.model_validate(created_record_data)

# Read de um registro inidividual
@router.get("/{record_id}", response_model=Record)
async def get_record(record_id: int):
    searched_record = db_records.read_one(record_id)
    if not searched_record:
        raise HTTPException(status_code=404, detail="Habit not found")
    return Record.model_validate(searched_record)

# Update
@router.put("/{record_id}", response_model=RecordUpdate)
async def update_record(record_id: int, record: RecordUpdate):
    record_update_data = record.model_dump()

    updated_data = db_records.update(record_id, record_update_data)

    if not updated_data:
        raise HTTPException(status_code=404, detail="Record with id {record_id} not found")
    return RecordUpdate.model_validate(updated_data)

# Delete
@router.delete("/{record_id}", status_code=204)
async def delete_record(record_id: int):
    success = db_records.delete(record_id);
    if not success:
        raise HTTPException(status_code=404, detail=f"Record with id: {record_id} not found.")
    db_records.vacuum()
    return

# Retorna página
@router.get("/", response_model=RecordsPaginationResponse)
async def get_users(page: int = Query(1, ge=1), page_size: int = Query(5, ge=1)):
    all_records = db_records.read()
    return paginate_data(all_records, page, page_size, Record)
