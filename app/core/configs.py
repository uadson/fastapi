from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
        Base Settings Application
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:admin@localhost:5432/high_school_db'
    DBBaseModel = declarative_base()

    class Config:
        case_sensitive = True


settings = Settings()
