from fastapi import APIRouter
from app.api.routes import users, habits, records


router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
