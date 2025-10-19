from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class HabitCreate(BaseModel):
    user_id: int
    name: str
    description: str
    frequence: str

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequence: Optional[str] = None
    deleted: Optional[bool] = None

    class Config:
        extra = "ignore"

class Habit(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    description: str
    frequence: str
    creation_date: Optional[datetime] = None
    deleted: bool

    class Config:
        from_atributes = True

class HabitsPaginationResponse(BaseModel):
    page: int
    page_size: int
    total: int
    habits: List[Habit]
