from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.db.models.user import User
from app.db.models.habit import Habit
from app.schemas.habit import HabitRead
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()

# Create
@router.post("/", response_model=UserRead)
async def create_user(user_in: UserCreate) -> UserRead:
    """
    Cria um novo usuário no sistema.
    Valida o schema de entrada e persiste o usuário no banco
    de dados.

    Args:
        user_in (UserCreate): Dados necessários para criação do usuário.

    Returns:
        UserRead: Usuário criado e persistido no banco de dados.
    """
    user = User(**user_in.model_dump())
    await user.insert()
    return UserRead.model_validate(user.model_dump())

# Update
@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: PydanticObjectId, user_up: UserUpdate) -> UserRead:
    """
    Atualiza parcialmente os dados de um usuário existente.

    Args:
        user_id (PydanticObjectId): Identificador do usuário a ser atualizado.
        user_up (UserUpdate): Dados para atualização do usuário.

    Returns:
        UserRead: Usuário atualizado.

    Raises:
        HTTPException:
            - 404: Usuário não encontrado.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_up.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await user.save()
    return UserRead.model_validate(user.model_dump())

# Delete
@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId) -> dict:
    """
    Exclui o usuário identificado pelo ID informado do banco de dados.

    Args:
        user_id (PydanticObjectId): Identificador do usuário a ser removido.

    Returns:
        dict: Mensagem confirmando a exclusão do usuário.

    Raises:
        HTTPException:
            - 404: Usuário não encontrado.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": f"User with id: {user_id} deleted."}

# Consultas
# Aggregation pipeline: conta habitos por usuário
@router.get("/habits-per-user")
async def count_habits_per_user():
    """
    Retorna a quantidade de hábitos cadastrados por usuário.

    Agrupa os hábitos pelo identificador do usuário e contabiliza
    o total de hábitos associados a cada um.

    Returns:
        list[dict]: Lista de objetos contendo o identificador do usuário
        (`_id`) e a quantidade total de hábitos (`count`) associada a ele.
    """
    pipeline = [
        { "$group": { "_id": "$user.$id", "count": { "$sum": 1 }}}
    ]
    result = await Habit.aggregate(pipeline).to_list()
    for doc in result:
        doc["_id"] = str(doc["_id"])
    return result

# Busca por texto parcial
@router.get("/search", response_model=Page[UserRead])
async def search_users(user_name: str) -> Page[UserRead]:
    """
    Busca usuários pelo nome.

    Este endpoint retorna uma lista paginada de usuários cujo campo `name`
    corresponde ao valor informado, utilizando uma busca por expressão regular.

    Args:
        user_name (str): Nome ou parte do nome do usuário a ser pesquisado.

    Returns:
        Page[UserRead]: Página contendo os usuários encontrados.
    """
    users = await apaginate(User.find({"name": {"$regex": user_name}}))
    return users

# Read
@router.get("/", response_model=Page[UserRead])
async def get_users() -> Page[UserRead]:
    """
    Retorna uma lista paginada de usuários.
    Utiliza paginação automática para listar os usuários
    cadastrados no banco de dados.

    Returns:
        Page[UserRead]: Página contendo a lista de usuários.
    """
    return await apaginate(User.find_all())

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: PydanticObjectId) -> UserRead:
    """
    Recupera um usuário específico pelo seu identificador.

    Args:
        user_id (PydanticObjectId): Identificador único do usuário.

    Returns:
        UserRead: Usuário correspondente ao ID informado.

    Raises:
        HTTPException:
            - 404: Usuário não encontrado.
    """
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserRead.model_validate(user.model_dump())

@router.get("/{user_id}/habits", response_model=Page[HabitRead])
async def get_habits_by_user(user_id: PydanticObjectId) -> Page[HabitRead]:
    """
    Lista hábitos associados a um usuário específico.

    Args:
        user_id (PydanticObjectId): Identificador único do usuário cujos
        hábitos serão consultados.

    Returns:
        Page[HabitRead]: Página contendo os hábitos relacionados ao usuário.
    """
    habits = await apaginate(Habit.find({"user.$id": user_id}))
    return habits

# Hábitos ativos mais recentes de usuario
@router.get("/{user_id}/habits/recent", response_model=Page[HabitRead])
async def get_recent_active_habits(user_id: PydanticObjectId) -> Page[HabitRead]:
    """
    Lista os hábitos ativos mais recentes de um usuário específico.

    Args:
        user_id (PydanticObjectId): Identificador único do usuário cujos
        hábitos ativos mais recentes serão consultados.

    Returns:
        Page[HabitRead]: Página contendo os hábitos ativos mais recentes
        relacionados ao usuário.
    """
    habits = await apaginate(Habit.find({"user.$id": user_id, "active": True}).sort("started_date"))
    return habits
