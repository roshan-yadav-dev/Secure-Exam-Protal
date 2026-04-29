from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App info
    APP_NAME: str = "AI Exam Platform"
    APP_VERSION: str = "1.0.0"

    # Mongo
    MONGO_URI: str
    DB_NAME: str

    # Auth
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()

APP_NAME = settings.APP_NAME
APP_VERSION = settings.APP_VERSION