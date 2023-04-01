from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:admin@localhost:5432/school'

    class Config:
        case_sensitive = True


settings: Settings = Settings()
