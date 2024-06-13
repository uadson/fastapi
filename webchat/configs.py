from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


class Settings:
    TEMPLATES = Jinja2Templates(directory='templates')
    STATICFILES = StaticFiles(directory='static')

settings: Settings = Settings()
