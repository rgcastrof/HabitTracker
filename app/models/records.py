from pydantic import BaseModel
from enum import Enum
from typing import Optional, List
from datetime import datetime

class RecordStatus(str, Enum):
    IN_PROGRESS = 'Em andamento'
    FINISHED = 'completado'
    FAILED = 'falhou'
    POSTPONED = 'adiado'
    SKIPPED = 'pulado'

class RecordCreate(BaseModel):
    habit_id: int
    status: RecordStatus
    observation: Optional[str] = None

class Record(BaseModel):
    id: Optional[int] = None
    habit_id: int
    timestamp: datetime
    status: RecordStatus
    observation: Optional[str] = None

    class Config:
        from_atributes = True

class RecordUpdate(BaseModel):
    status: Optional[RecordStatus] = None
    observation: Optional[str] = None

    class Config:
        extra = "ignore"

class RecordsPaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int
    items: List[Record]
