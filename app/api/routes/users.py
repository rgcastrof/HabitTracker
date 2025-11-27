from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserRead
from app.models.user import User
from sqlmodel import Session
from app.core.database import get_session

router = APIRouter()

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
