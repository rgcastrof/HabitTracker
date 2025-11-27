from fastapi import APIRouter, Depends, HTTPException, Query
from app.schemas.user import UserCreate, UserRead
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
