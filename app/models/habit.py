from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Habit(BaseModel):
    id: Optional[int] = None
    user_id: int
    name: str
    description: str
    frequence: str
    creation_date: Optional[datetime] = None
