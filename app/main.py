from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.habit import router as habit_router
from app.routers.records import router as record_router
from app.routers.utils import router as utils_router

app = FastAPI()
app.include_router(utils_router)
app.include_router(user_router)
app.include_router(habit_router)
app.include_router(record_router)

@app.get("/")
async def root():
    return {"message": "API Habit Tracker está rodando!"}
