from fastapi import APIRouter
from api.routes import users
from api.routes import habits
from api.routes import records

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(habits.router, prefix="/habits", tags=["Habits"])
router.include_router(records.router, prefix="/records", tags=["Records"])
