import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_TOKEN: str = os.getenv("API_TOKEN", "secure_token")
    REDIS_HOST: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
