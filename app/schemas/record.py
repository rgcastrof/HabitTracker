from datetime import datetime
from pydantic import BaseModel
from app.enums.Status import Status

class RecordCreate(BaseModel):
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

class RecordRead(BaseModel):
    """
    Schema para leitura de registro

    Representa os dados retornados pela API ao consultar registro

    Attributes:
        status (Status): Status de conclusão registrado
        value (float): Valor/quantidade do hábito registrado
        comment (str | None): Comentário opcional para registro
        creation_date (datetime): Data de criação do registro
    """
    status: Status
    value: float
    comment: str | None
    creation_date: datetime

class RecordUpdate(BaseModel):
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
