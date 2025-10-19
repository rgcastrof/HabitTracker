from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.habit import router as habit_router
from app.utils.router_utils import router as export_router

app = FastAPI()
app.include_router(export_router)
app.include_router(user_router)
app.include_router(habit_router)

@app.get("/")
async def root():
    return {"message": "API Habit Tracker está rodando!"}
