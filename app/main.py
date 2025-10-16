from fastapi import FastAPI
from app.routers.user import router as user_router

app = FastAPI()
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "API Habit Tracker está rodando!"}
