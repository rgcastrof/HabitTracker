from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    """
    Schema para criação de usuário.
    Utilizado para validação de dados de entrada ao criar um novo usuário.

    Attributes:
        name (str): Nome do usuário
        email (EmailStr): Email do usuário
        password (str): Senha do usuário
    """
    name: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    """
    Schema para leitura de usuário.
    Representa os dados retornados pela API ao consultar usuários.

    Attributes:
        id (str): Identificador único do usuário no MongoDB
        name (str): Nome do usuário
        email (EmailStr): Email do usuário
        creation_date (datetime): Data de criação do usuário
    """
    id: str
    name: str
    email: EmailStr
    creation_date: datetime

class UserUpdate(BaseModel):
    """
    Schema para atualização de usuário.

    Utilizado para validação de dados de entrada ao atualizar o usuário.
    Todos os campos são opcionais.
    
    Attributes:
        name (str): Novo nome do usuário
        email (EmailStr): Novo email do usuário
        password (str): Nova senha do usuário
    """
    name: str | None
    email: EmailStr | None
    password: str | None
