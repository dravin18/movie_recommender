from pydantic_settings import BaseSettings
from pathlib import Path
env_path = Path('.')/".env"

class Settings(BaseSettings):
    secret_key : str
    algorithm: str
    mongodb_port: str
    access_token_expire_minutes: int
    mongodb_database_name: str
    movie_collection_name: str
    users_collection_name: str
    rating_collection_name: str
    mongodb_host_name: str

    class Config:
        env_file = env_path

settings = Settings()