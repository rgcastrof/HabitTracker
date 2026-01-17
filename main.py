from fastapi import FastAPI
from fastapi_pagination import add_pagination
from app.db.client import init_db, close_db
from contextlib import asynccontextmanager
from api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(title="Habit Tracker API", lifespan=lifespan)
app.include_router(router)
add_pagination(app)

@app.get("/")
def root():
    """
    Endpoint raiz da API

    Retorna uma mensagem simples para verificar se a API está rodando

    Returns:
        dict: Mensagem de status da API
    """
    return {"message": "Habit Tracker API is still working"}
