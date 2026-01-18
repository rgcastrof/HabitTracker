from fastapi import APIRouter, HTTPException
from beanie import PydanticObjectId
from fastapi_pagination import Page
from fastapi_pagination.ext.beanie import apaginate
from app.db.models.user import User
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
