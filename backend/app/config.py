from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DATABASE_URL: str = "postgresql+asyncpg://baro:baro_local@localhost:5432/baro"
    REDIS_URL: str = "redis://localhost:6379/0"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    NAVER_CLIENT_ID: str = ""
    NAVER_CLIENT_SECRET: str = ""
    GOOGLE_API_KEY: str = ""
    GOOGLE_CSE_ID: str = ""

    BATCH_SCHEDULE_HOURS: list[int] = [9, 18]
    DAILY_COLLECTION_LIMIT: int = 500
    LOG_LEVEL: str = "INFO"


settings = Settings()
