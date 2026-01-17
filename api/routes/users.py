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
    user = User(**user_in.model_dump())
    await user.insert()
    assert user.id is not None
    return UserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        creation_date=user.creation_date
    )

# Read
@router.get("/", response_model=Page[UserRead])
async def get_users() -> Page[UserRead]:
    return await apaginate(User.find_all())

@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: PydanticObjectId) -> UserRead:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    assert user.id is not None
    return UserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        creation_date=user.creation_date
    )

# Update
@router.put("/{user_id}", response_model=UserRead)
async def update_user(user_id: PydanticObjectId, user_up: UserUpdate) -> UserRead:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_up.model_dump(exclude_none=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await user.save()
    assert user.id is not None
    return UserRead(
        id=user.id,
        name=user.name,
        email=user.email,
        creation_date=user.creation_date
    )

# Delete
@router.delete("/{user_id}")
async def delete_user(user_id: PydanticObjectId) -> dict:
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await user.delete()
    return {"message": f"User with id: {user_id} deleted."}
