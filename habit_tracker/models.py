from pydantic import BaseModel, EmailStr
from enum import Enum
from typing import Optional
from datetime import datetime

class RecordStatus(Enum):
    FINISHED = 'completado'
    FAILED = 'falhou'
    POSTPONED = 'adiado'
    SKIPPED = 'pulado'

class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    passwd: str
    register_date: datetime
    active: bool

class Habit(BaseModel):
    id: int
    user_id: int
    name: str
    description: str
    frequence: str
    creation_date: datetime

class Record(BaseModel):
    id: int
    habit_id: int
    timestamp: datetime
    status: RecordStatus
    observation: Optional[str] = None
