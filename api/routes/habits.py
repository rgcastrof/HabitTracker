from fastapi import APIRouter, HTTPException, Query
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.db.models.habit import Habit
from app.db.models.record import Record
from app.db.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.record import RecordRead

router = APIRouter()

# Create
@router.post("/", response_model=HabitRead)
async def create_habit(user_id: PydanticObjectId, habit_in: HabitCreate) -> HabitRead:
    """
    Cria um novo hábito associado a um usuário.
    O hábito é persistido no banco e retornado após a inserção.

    Args:
        user_id (PydanticObjectId): Identificador do usuário dono do hábito.
        habit_in (HabitCreate): Dados necessários para criação do hábito.

    Returns:
        HabitRead: Hábito criado e persistido no banco de dados.

    Raises:
        HTTPException:
            - 404: Usuário não encontrado.
            - 500: Hábito foi inserido, mas não pôde ser recuperado.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    habit_new = Habit(**habit_in.model_dump(), user=user)  # type: ignore
    await habit_new.insert()
    inserted = await Habit.get(habit_new.id)
    if not inserted:
        raise HTTPException(status_code=500, detail="Habit inserted but could not be loaded")

    return HabitRead.model_validate(inserted.model_dump())

# Update
@router.put("/{habit_id}", response_model=HabitRead)
async def update_habit(habit_id: PydanticObjectId, habit_up: HabitUpdate) -> HabitRead:
    """
    Atualiza parcialmente os dados de um hábito existente.

    Args:
        habit_id (PydanticObjectId): Identificador do hábito a ser atualizado.
        habit_up (HabitUpdate): Dados para atualização do hábito.

    Returns:
        HabitRead: Hábito atualizado.

    Raises:
        HTTPException:
            - 404: Hábito não encontrado.
    """
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    update_data = habit_up.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(habit, key, value)

    await habit.save()
    return HabitRead.model_validate(habit.model_dump())

# Delete
@router.delete("/{habit_id}")
async def delete_habit(habit_id: PydanticObjectId) -> dict:
    """
    Remove um hábito do banco de dados.

    Args:
        habit_id (PydanticObjectId): Identificador do hábito a ser removido.

    Returns:
        dict: Mensagem confirmando a exclusão do hábito.

    Raises:
        HTTPException:
            - 404: Hábito não encontrado.
    """
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")

    await habit.delete()
    return {"message": f"Habit with id: {habit_id} deleted."}

# Consultas
# Busca por texto parcial
@router.get("/search", response_model=Page[HabitRead])
async def search_habits(habit_name: str = "") -> Page[HabitRead]:
    """
    Busca hábitos pelo nome.

    Este endpoint retorna uma lista paginada de hábitos cujo campo `name`
    corresponde ao valor informado, utilizando uma busca por expressão regular.

    Args:
        habit_name (str): Nome ou parte do nome do hábito a ser pesquisado.

    Returns:
        Page[HabitRead]: Página contendo os hábitos encontrados.
    """
    habits = await apaginate(Habit.find({"name": {"$regex": habit_name}}))
    return habits

# Read
@router.get("/", response_model=Page[HabitRead])
async def get_habits() -> Page[HabitRead]:
    """
    Retorna uma lista paginada de hábitos.

    Utiliza paginação automática para retornar os hábitos
    cadastrados no banco de dados.

    Returns:
        Page[HabitRead]: Página contendo a lista de hábitos.
    """
    return await apaginate(Habit.find_all())

@router.get("/{habit_id}", response_model=HabitRead)
async def get_habit(habit_id: PydanticObjectId) -> HabitRead:
    """
    Recupera um hábito específico pelo seu identificador.

    Args:
        habit_id (PydanticObjectId): Identificador único do hábito.

    Returns:
        HabitRead: Hábito correspondente ao ID informado.

    Raises:
        HTTPException:
            - 404: Hábito não encontrado.
    """
    habit = await Habit.get(habit_id)
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    return HabitRead.model_validate(habit.model_dump())

# Listagem filtrada por relacionamento
@router.get("/{habit_id}/records", response_model=Page[RecordRead])
async def get_records_by_habit(habit_id: PydanticObjectId) -> Page[RecordRead]:
    """
    Lista registros associados a um hábito específico.

    Args:
        habit_id (PydanticObjectId): Identificador único do hábito cujos
        registros serão consultados.

    Returns:
        Page[RecordRead]: Página contendo os registros relacionados ao hábito.
    """
    records = await apaginate(Record.find({"habit.$id": habit_id}))
    return records
