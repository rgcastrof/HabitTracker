from sqlmodel import SQLModel, Field, Relationship, Enum as SAEnum
from datetime import datetime, timezone
from app.enums import Frequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .record import Record

class HabitBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    description: str | None = Field(max_length=255)
    active: bool = Field(default=True)
    started_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    frequence: Frequence | None = Field(
        default=None,
        sa_column=SAEnum(Frequence, name="frequence_enum"),
    )

class Habit(HabitBase, table=True):
    user_id: int = Field(foreign_key="user.id")
    user: 'User' = Relationship(back_populates="habits")
    records: list['Record'] = Relationship(back_populates="habit")
