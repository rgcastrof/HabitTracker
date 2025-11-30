from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
    Configurações da aplicação carregadas de variáveis de ambiente

    Esta classe utiliza Pydantic BaseSettings para ler as configurações
    automaticamente do arquivo '.env'

    Attributes:
        DATABASE_URL (str): URL de conexão com o banco de dados
    """
    DATABASE_URL: str

    class Config:
        """Configurações internas do pydantic para leitura de .env"""
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
