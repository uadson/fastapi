from decouple import config


class Settings:
    URL_DEPARTMENTS = config('URL_DEPARTMENTS')
    
settings: Settings = Settings()
