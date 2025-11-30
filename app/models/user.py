from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .habit import Habit

class UserBase(SQLModel):
    """
    Modelo base de usuário com campos comuns

    Attributes:
        id (int | None): Identificar único de usuário, chave primária
        name (str): Nome do usuário (máximo 50 caracteres)
        email (str): Email do usuário (máximo 100 caracteres)
        password (str): Senha do usuário (máximo 50 caracteres)
        creation_date (datetime): Data de criação da conta
    """
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    email: str = Field(max_length=100)
    password: str = Field(max_length=50)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class User(UserBase, table=True):
    """
    Modelo de usuário que representa a tabela no banco

    Extende UserBase e adiciona relacionamento com hábitos

    Attributes:
        habits (list[Habits]): Lista de hábitos associados ao usuário
    """
    habits: list['Habit'] = Relationship(back_populates="user", cascade_delete=True)
