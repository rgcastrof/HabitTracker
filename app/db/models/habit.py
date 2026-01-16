from datetime import datetime, timezone
from beanie import Document, Link
from pydantic import Field
from app.db.models.user import User
from app.enums.Frequence import Frequence

class Habit(Document):
    """
    Documento do MongoDB que representa um hábito.

    Attributes:
        name (str): Nome do hábito (máximo 50 caracteres)
        description (str | None): Descrição opcional do hábito (máximo 255 caracteres)
        active (bool): Indica se o hábito está ativo. Padrão é True
        started_date (datetime): Data de início de rastreio do hábito
        frequence: (Frequence | None) Frequencia de execução do hábito (daily, weekly, monthly)
        user: (Link[User]): Referência ao usuário que possui o hábito
    """
    name: str = Field(max_length=50)
    description: str | None = Field(max_length=255)
    active: bool = Field(default=True)
    started_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    frequence: Frequence | None = Field(default=None)
    user: Link[User]

    class Settings:
        name = "habits"
