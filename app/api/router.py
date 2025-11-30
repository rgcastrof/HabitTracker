from fastapi import APIRouter
from app.api.routes import users, habits, records


router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(habits.router, prefix="/habits", tags=["Habits"])
router.include_router(records.router, prefix="/records", tags=["Records"])
