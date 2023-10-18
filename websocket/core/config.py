from fastapi.templating import Jinja2Templates


class Settings:
    TEMPLATES = Jinja2Templates(directory="templates")
    
settings: Settings=Settings()
