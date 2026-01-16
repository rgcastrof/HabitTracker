from datetime import datetime, timezone
from beanie import Document, Link
from pydantic import Field
from app.db.models.habit import Habit
from app.enums.Status import Status

class Record(Document):
    """
    Documento do MongoDB que representa um registro.

    Attributes:
        value (float): Valor/quantidade do hábito registrado (Ex: 20 páginas lidas)
        status (Status): Status de conclusão registrado (finished, partially, unfinished)
        comment (str | None): Comentário opcional para registro
        creation_date (datetime): Data de criação do registro
        habit: (Link[Habit]): Referência ao hábito que possui o registro
    """
    value: float
    status: Status
    comment: str | None = Field(default = None, max_length=255)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    habit: Link[Habit]
    
    class Settings:
        name = "records"
