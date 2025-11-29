from datetime import datetime
from sqlmodel import SQLModel
from app.enums import Status

class RecordCreate(SQLModel):
    value: float
    status: Status
    comment: str | None

class RecordRead(SQLModel):
    id: int
    status: Status | None
    value: float | None
    comment: str | None
    creation_date: datetime

class RecordUpdate(SQLModel):
    valued: float | None
    status: Status | None
    comment: str | None
