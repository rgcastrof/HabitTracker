from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(settings.DATABASE_URL)  # Cria o engine com a url puxada da classe Settings

def create_db_and_tables() -> None:
    """
    Cria todas as tabelas do banco de dados definidas nos modelos SQLModel

    Esta função deve ser chamada apenas uma vez, na inicialização da aplicação
    """
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    """
    Cria e retorna uma sessão de conexão com o banco

    Returns:
        Session: Sessão do SQLAlchemy ligada ao engine configurado
    """
    return Session(engine)
