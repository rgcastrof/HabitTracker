from beanie import PydanticObjectId
from pydantic import BaseModel
from datetime import datetime
from app.enums.Frequence import Frequence

class HabitCreate(BaseModel):
    """
    Schema para criação de hábito

    Utilizado para validação de dados de entrada ao criar um novo hábito

    Attributes:
        name (str): Nome do hábito
        description (str | None): descrição opcional do hábito
        active (bool): Indica se o hábito está ativo
        Frequence: (Frequence | None) Frequencia de execução do hábito
    """
    name: str
    description: str | None
    active: bool
    frequence: Frequence | None

class HabitRead(BaseModel):
    """
    Schema para leitura de hábito

    Representa os dados retornados pela API ao consultar hábito

    Attributes:
        id (PydanticObjectId): Identificador único de hábito
        name (str): Nome do hábito
        description (str | None): Descrição opcional do hábito
        active (bool): Indica se o hábito está ativo
        Frequence: (Frequence | None) Frequencia de execução do hábito
        started_date (datetime): Data de incío de rastreio do hábito
    """
    id: PydanticObjectId
    name: str
    description: str | None
    active: bool
    frequence: Frequence | None
    started_date: datetime

class HabitUpdate(BaseModel):
    """
    Schema para atualização de hábito

    Utilizado para validação de dados de entrada ao atualizar o hábito
    Todos os campos são opcionais

    Attributes:
        name (str | None): Novo nome do hábito
        description (str | None): Nova descrição do hábito
        active (bool | None): Novo status do hábito
        Frequence: (Frequence | None) Nova frequência de execução do hábito
    """
    name: str | None
    description: str | None
    active: bool | None
    frequence: Frequence | None
