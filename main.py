from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def home():
    return {"msg": "Habit Tracker API funcionando" }
