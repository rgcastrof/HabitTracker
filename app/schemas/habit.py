from datetime import datetime
from sqlmodel import SQLModel

from app.enums import Frequence

class HabitCreate(SQLModel):
    name: str
    description: str | None
    active: bool
    frequence: Frequence | None

class HabitRead(SQLModel):
    id: int
    name: str
    description: str | None
    active: bool
    frequence: Frequence | None
    started_date: datetime
