from datetime import datetime, timezone
from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.db.models.habit import Habit
from app.db.models.record import Record
from app.schemas.record import RecordCreate, RecordRead, RecordUpdate

router = APIRouter()

# Create
@router.post("/", response_model=RecordRead)
async def create_record(habit_id: PydanticObjectId, record_in: RecordCreate) -> RecordRead:
    """
    Cria um novo registro associado a um hábito.

    Args:
        habit_id (PydanticObjectId): Identificador do hábito ao qual o registro pertence.
        record_in (RecordCreate): Dados necessários para criação do registro.

    Returns:
        RecordRead: Registro criado e persistido no banco de dados.

    Raises:
        HTTPException:
            - 404: Hábito não encontrado.
    """
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    record = Record(**record_in.model_dump(), habit=habit)  # type: ignore
    await record.insert()
    return RecordRead.model_validate(record.model_dump())

# Update
@router.put("/{record_id}", response_model=RecordRead)
async def update_record(record_id: PydanticObjectId, record_up: RecordUpdate) -> RecordRead:
    """
    Atualiza parcialmente os dados de um registro existente.

    Args:
        record_id (PydanticObjectId): Identificador do registro a ser atualizado.
        record_up (RecordUpdate): Dados para atualização do registro.

    Returns:
        RecordRead: Registro atualizado.

    Raises:
        HTTPException:
            - 404: Registro não encontrado.
    """
    record = await Record.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    update_data = record_up.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(record, key, value)

    await record.save()
    return RecordRead.model_validate(record.model_dump())

# Delete
@router.delete("/{record_id}")
async def delete_record(record_id: PydanticObjectId) -> dict:
    """
    Remove um registro do banco de dados.
    Exclui o registro identificado pelo ID informado do banco de dados.

    Args:
        record_id (PydanticObjectId): Identificador do registro a ser removido.

    Returns:
        dict: Mensagem confirmando a exclusão do registro.

    Raises:
        HTTPException:
            - 404: Registro não encontrado.
    """
    record = await Record.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    await record.delete()
    return {"message": f"Record with id: {record_id} deleted."}

# Consultas
# Consulta por data
@router.get("/date", response_model=Page[RecordRead])
async def get_records_by_date(
    year: int,
    month: int,
    start: int,
    end: int
) -> Page[RecordRead]:
    """
    Retorna registros do banco de dados filtrados por intervalo de datas.

    Args:
        year (int): Ano da data de criação dos registros.
        month (int): Mês da data de criação dos registros.
        start (int): Dia inicial do intervalo de busca.
        end (int): Dia final do intervalo de busca.

    Returns:
        Page[RecordRead]: Lista paginada de registros encontrados no intervalo informado.

    Raises:
        HTTPException:
            - 400: Intervalo de datas inválido.
    """
    start_datetime = datetime(year, month, start, tzinfo=timezone.utc)
    end_datetime = datetime(year, month, end, tzinfo=timezone.utc)
    records = await apaginate(Record.find(
        {"creation_date": {
            "$gte": start_datetime,
            "$lte": end_datetime
        }}
    ))
    return records


# Read
@router.get("/", response_model=Page[RecordRead])
async def get_records() -> Page[RecordRead]:
    """
    Retorna uma lista paginada de registros.

    Returns:
        Page[RecordRead]: Página contendo a lista de registros.
    """
    return await apaginate(Record.find_all())

@router.get("/{record_id}", response_model=RecordRead)
async def get_record(record_id: PydanticObjectId) -> RecordRead:
    """
    Retorna um registro específico pelo seu identificador.

    Args:
        record_id (PydanticObjectId): Identificador único do registro.

    Returns:
        RecordRead: Registro correspondente ao ID informado.

    Raises:
        HTTPException:
            - 404: Registro não encontrado.
    """
    record = await Record.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return RecordRead.model_validate(record.model_dump())
