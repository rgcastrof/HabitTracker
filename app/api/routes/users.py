from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.models.user import User
from sqlmodel import Session, select
from app.core.database import get_session

router = APIRouter()

# CRUD Operations
# Create
@router.post("/", response_model=UserRead)
async def create_user(user: UserCreate, db: Session = Depends(get_session)):
    try:
        db_user = User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        print(f"Erro ao criar usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

# Read (all)
@router.get("/", response_model=list[UserRead])
async def list_users(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=10, le=100),
    db: Session = Depends(get_session)
):
    stmt = select(User).offset(offset).limit(limit)
    return db.exec(stmt).all()

# Read (one)
@router.get("/{user_id}", response_model=UserRead)
async def get_user(user_id: int, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, detail="Usuário não encontrado")
    return user

# Update
@router.patch("/{user_id}", response_model=UserRead)
async def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(404, detail="Usuário não encontrado")

    if user_update.name is not None:
        if user_update.name.strip() == "":
            raise HTTPException(status_code=400, detail="Nome não pode ser vazio")
        user.name = user_update.name
    if user_update.email is not None:
        if user_update.email.strip() == "":
            raise HTTPException(status_code=400, detail="Email não pode ser vazio")
        user.email = user_update.email
    if user_update.password is not None:
        if user_update.password.strip() == "":
            raise HTTPException(status_code=400, detail="Senha não pode ser vazio")
        user.password = user_update.password

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        print(f"Erro ao atualizar dados do usuário: {e}")
        raise HTTPException(status_code=500, detail="Erro ao atualizar dados do usuário")
