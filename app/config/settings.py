import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Vera Merchant AI Assistant"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DATA_DIR: str = "data"
    LOG_LEVEL: str = "INFO"
    LLM_API_KEY: str = ""
    LLM_PROVIDER: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()
