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

class HabitUpdate(SQLModel):
    name: str | None
    description: str | None
    active: bool | None
    frequence: Frequence | None

class ActiveHabitsResponse(SQLModel):
    user_id: int
    completed_habits: int
