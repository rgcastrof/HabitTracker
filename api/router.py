from fastapi import APIRouter
from api.routes import users

router = APIRouter()
router.include_router(users.router, prefix="/users", tags=["Users"])
