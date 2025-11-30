from datetime import datetime
from sqlmodel import SQLModel
from app.enums import Status

class RecordCreate(SQLModel):
    """
    Schema para criação de registro no banco

    Utilizado para validação de dados de entrada ao criar um novo registro

    Attributes:
        value (float): Valor/quantidade do hábito registrado
        status (Status): Status de conclusão registrado
        comment (str | None): Comentário opcional para registro
    """
    value: float
    status: Status
    comment: str | None

class RecordRead(SQLModel):
    """
    Schema para leitura de registro

    Representa os dados retornados pela API ao consultar registro

    Attributes:
        id (int): Identificador único de registro
        status (Status): Status de conclusão registrado
        value (float): Valor/quantidade do hábito registrado
        comment (str | None): Comentário opcional para registro
        creation_date (datetime): Data de criação do registro
    """
    id: int
    status: Status
    value: float
    comment: str | None
    creation_date: datetime

class RecordUpdate(SQLModel):
    """
    Schema para atualização de registro

    Utilizado para validação de dados de entrada ao atualizar o registro
    Todos os campos são opcionais

    Attributes:
        value (float | None): Valor/quantidade do hábito registrado
        status (Status | None): Status de conclusão registrado
        comment (str | None): Comentário opcional para registro
    """
    value: float | None
    status: Status | None
    comment: str | None
