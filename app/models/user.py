from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .habit import Habit

class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=100, unique=True)
    password: str = Field(max_length=50)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(UserBase, table=True):
    habits: list['Habit'] = Relationship(back_populates="user")
