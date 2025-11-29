from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Enum as SAEnum
from app.enums import Status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .habit import Habit

class RecordBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    value: float
    status: Status = Field(sa_column=SAEnum(name="status_enum"))
    comment: str | None = Field(max_length=255)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Record(RecordBase, table=True):
    habit_id: int = Field(foreign_key="habit.id")
    habit: 'Habit' = Relationship(back_populates="records")
