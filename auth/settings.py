from pydantic import PostgresDsn, KafkaDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    auth_db_url: PostgresDsn
    auth_root_password: str
    kafka_url: str


settings = Settings()
