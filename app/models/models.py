from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Enum as sqlEnum
from typing import List
from datetime import datetime, timezone
from enum import Enum

class Base(DeclarativeBase):
    pass

class Frequence(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"

class Status(Enum):
    FINISHED = "completed"
    PARTIALLY = "partially"
    UNFINISHED = "unfinished"


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(50))
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    habits: Mapped[List["Habit"]] = relationship(  # type: ignore[reportUndefineVariable]
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"User(id={self.id}, name={self.name}, email={self.email})"

class Habit(Base):
    __tablename__ = "habit"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    active: Mapped[bool] = mapped_column(default=True)
    started_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))
    frequence: Mapped[Frequence | None] = mapped_column(
        sqlEnum(Frequence, name="frequence_enum"), nullable=True
    )

    user: Mapped[User] = relationship(back_populates="habits")
    records: Mapped[List["Record"]] = relationship(
        back_populates="habit", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Habit(id={self.id}, name={self.name}, description={self.description})"

class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    habit_id: Mapped[int] = mapped_column(ForeignKey("habit.id", ondelete="CASCADE"))
    status: Mapped[Status] = mapped_column(sqlEnum(Status, name="status_enum"))
    value: Mapped[float | None] = mapped_column(nullable=True)
    commentary: Mapped[str | None] = mapped_column(String(255), nullable=True)
    creation_date: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    habit: Mapped[Habit] = relationship(back_populates="records")

    def __repr__(self) -> str:
        return f"Record(id={self.id}, status={self.status})"
