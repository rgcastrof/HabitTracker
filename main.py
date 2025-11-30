from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.api.router import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager assíncrono que define o lifespan da aplicação

    Cria todas as tabelas do banco de dados ao iniciar a aplicação

    Args:
        app (FastAPI): Instância da aplicação FastAPI
    """
    create_db_and_tables()
    yield

app = FastAPI(title="Habit Tracker API", lifespan=lifespan)
app.include_router(router)  # inclui router com todos os endpoints da API

@app.get("/")
def root():
    """
    Endpoint raiz da API

    Retorna uma mensagem simples para verificar se a API está rodando

    Returns:
        dict: Mensagem de status da API
    """
    return {"message": "Habit Tracker API is still working"}
