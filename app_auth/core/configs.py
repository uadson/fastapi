from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base


class Settings(BaseSettings):
    """
        Base Settings Application
    """
    API_V1_STR: str = '/api/v1'
    DB_URL: str = 'postgresql+asyncpg://postgres:admin@localhost:5432/high_school'
    DBBaseModel = declarative_base()

    JWT_SECRET: str = 'rGvyW2TeuWQe_pwmDP8AQRGCF2Y0TSuXtro75S4a6NE'
    
    """
    import secrets

    token: str = secrets.token_urlsafe(32)
    """
    ALGORITHM: str = 'HS256'

    # 60 minutes * 24 hours * 7 days => 1 week
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    class Config:
        case_sensitive = True


settings: Settings = Settings()
