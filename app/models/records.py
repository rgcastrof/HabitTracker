from pydantic import BaseModel
from enum import Enum
from typing import Optional
from datetime import datetime

class RecordStatus(Enum):
    FINISHED = 'completado'
    FAILED = 'falhou'
    POSTPONED = 'adiado'
    SKIPPED = 'pulado'

class Record(BaseModel):
    id: Optional[int] = None
    habit_id: int
    timestamp: datetime
    status: RecordStatus
    observation: Optional[str] = None
