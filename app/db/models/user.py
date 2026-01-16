from beanie import Document
from pydantic import Field, EmailStr
from datetime import datetime, timezone

class User(Document):
    """
    Documento do MongoDB que representa um usuário.

    Attributes:
        name (str): Nome do usuário (máximo 50 caracteres)
        email (EmailStr): Email do usuário (máximo 100 caracteres)
        password (str): Senha do usuário (máximo 50 caracteres)
        creation_date (datetime): Data de criação da conta
    """
    name: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str = Field(max_length=50)
    creation_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "users"
