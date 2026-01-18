from fastapi import APIRouter
from api.routes import users
from api.routes import habits

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(habits.router, prefix="/habits", tags=["Habits"])
