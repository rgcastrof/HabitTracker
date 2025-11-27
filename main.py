from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(title="Habit Tracker API", lifespan=lifespan)
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Habit Tracker API is still working"}
