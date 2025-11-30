from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship, Enum as SAEnum
from app.enums import Status
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .habit import Habit

class RecordBase(SQLModel):
    """
    Modelo base de registro com campos comuns

    Attributes:
        id (int | None): Identificador único de registro, chave primária
        value (float): Valor/quantidade do hábito registrado (Ex: 20 páginas lidas)
        status (Status): Status de conclusão registrado (finished, partially, unfinished)
        comment (str | None): Comentário opcional para registro
        creation_date (datetime): Data de criação do registro
    """
    id: int | None = Field(default=None, primary_key=True)
    value: float
    status: Status = Field(sa_column=SAEnum(name="status_enum"))
    comment: str | None = Field(max_length=255)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Record(RecordBase, table=True):
    """
    Modelo de registro que representa tabela no banco de dados

    Extende RecordBase e adiciona relacionamento com hábito

    Attributes:
        habit_id (int): Chave estrangeira que referencia hábito
        habit (Habit): Objeto Habit relacionado ao hábito
    """
    habit_id: int = Field(foreign_key="habit.id")
    habit: 'Habit' = Relationship(back_populates="records")
