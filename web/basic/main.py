from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import UploadFile
from pathlib import Path
from aiofile import async_open

from uuid import uuid4

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')
media = Path('media')


@app.get('/')
async def index(request: Request, user: str = 'Felicity Jones'):
    context = {
        'request': request,
        'user': user
    }

    return templates.TemplateResponse('index.html', context=context)


@app.get('/servicos')
async def servicos(request: Request):
    context = {
        'request': request,
     }

    return templates.TemplateResponse('services.html', context=context)


@app.post('/servicos')
async def cad_servicos(request: Request):
    form = await request.form()
    service: str = form.get('servico')

    file: UploadFile = form.get('file')
    
    # print(f'Serviço: {service}')
    # print(f'Nome do arquivo: {file.filename}')
    # print(f'Tipo do arquivo: {file.content_type}')

    file_ext: str = file.filename.split('.')[1]
    new_name: str = f"{str(uuid4())}.{file_ext}"
    
    context = {
        'request': request,
        'image': new_name
    }

    async with async_open(f"{media}/{new_name}", "wb") as afile:
        await afile.write(file.file.read())

    return templates.TemplateResponse('services.html', context=context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
