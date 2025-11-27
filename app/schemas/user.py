from sqlmodel import SQLModel
from datetime import datetime

class UserCreate(SQLModel):
    name: str
    email: str
    password: str

class UserRead(SQLModel):
    id: int
    name: str
    email: str
    creation_date: datetime
