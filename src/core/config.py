from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='../.env', env_file_encoding='utf-8')

    # server
    SERVER_HOST: str = "localhost"
    SERVER_PORT: int = 8000

    # databases
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "TableReservation"
    DB_SOCKET: str = "localhost"
    DB_LOGS: bool = False

    # redis
    REDIS_SOCKET: str = "localhost"


settings = Settings()
