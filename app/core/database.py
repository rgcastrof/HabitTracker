from sqlmodel import SQLModel, create_engine, Session
from dotenv import load_dotenv
load_dotenv()
from config import settings
import logging

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_engine(settings.DATABASE_URL)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)

def get_session() -> Session:
    return Session(engine)
