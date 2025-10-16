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
    id: Optional[int] = None
    name: str
    email: EmailStr
    passwd: str
    register_date: Optional[datetime] = None
    active: bool

class Habit(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    description: str
    frequence: str
    creation_date: Optional[datetime] = None

class Record(BaseModel):
    id: Optional[int] = None
    habit_id: int
    timestamp: datetime
    status: RecordStatus
    observation: Optional[str] = None
