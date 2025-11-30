from sqlmodel import SQLModel, Field, Relationship, Enum as SAEnum
from datetime import datetime, timezone
from app.enums import Frequence
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
    from .record import Record

class HabitBase(SQLModel):
    """
    Modelo base de hábito com campos comuns

    Attributes:
        id (int | None): Identificador único de hábito, chave primária
        name (str): Nome do hábito (máximo 50 caracteres)
        description (str | None): Descrição opcional do hábito (máximo 255 caracteres)
        active (bool): Indica se o hábito está ativo. Padrão é True
        started_date (datetime): Data de incío de rastreio do hábito
        Frequence: (Frequence | None) Frequencia de execução do hábito (daily, weekly, monthly)
    """

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
    """
    Modelo de hábito que representa a tabela no banco de dados

    Extende HabitBase e adiciona relacionamentos com usuário e registro

    Attributes:
        user_id (int): Chave estrangeira que referencia usuário dono do hábito
        user (User): Objeto User relacionado ao usuário
        records (list[Record]): Lista de registros associados ao hábito
    """
    user_id: int = Field(foreign_key="user.id")
    user: 'User' = Relationship(back_populates="habits")
    records: list['Record'] = Relationship(back_populates="habit", cascade_delete=True)
