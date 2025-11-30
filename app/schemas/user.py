from sqlmodel import SQLModel
from datetime import datetime

class UserCreate(SQLModel):
    """
    Schema para criação de usuário

    Utilizado para validação de dados de entrada ao criar um novo usuário

    Attributes:
        name (str): Nome do usuário
        email (str): Email do usuário
        password (str): Senha do usuário
    """
    name: str
    email: str
    password: str

class UserRead(SQLModel):
    """
    Schema para leitura de usuário

    Representa os dados retornados pela API ao consultar usuários

    Attributes:
        id (int): Identificador do usuário
        name (str): Nome do usuário
        email (str): Email do usuário
        creation_date (datetime): Data de criação do usuário
    """
    id: int
    name: str
    email: str
    creation_date: datetime

class UserUpdate(SQLModel):
    """
    Schema para atualização de usuário

    Utilizado para validação de dados de entrada ao atualizar o usuário
    Todos os campos são opcionais
    
    Attributes:
        name (str): Novo nome do usuário
        email (str): Novo email do usuário
        password (str): Nova senha do usuário
    """
    name: str | None
    email: str | None
    password: str | None
