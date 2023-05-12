from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request

app = FastAPI()
templates = Jinja2Templates(directory='templates')
app.mount('/static', StaticFiles(directory='static'), name='static')
app.mount('/media', StaticFiles(directory='media'), name='media')


@app.get('/', name='index')
async def index(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('home/index.html', context=context)


@app.get('/about', name='about')
async def about(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('about/about.html', context=context)


@app.get('/contact', name='contact')
async def contact(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('contact/contact.html', context=context)


@app.get('/pricing', name='pricing')
async def pricing(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('pricing/pricing.html', context=context)


@app.get('/faq', name='faq')
async def faq(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('faq/faq.html', context=context)


@app.get('/blog', name='blog_home')
async def blog_home(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('blog/home/home.html', context=context)


@app.get('/blog/posts', name='blog_post')
async def blog_post(request: Request):
    context = {
        'request': request
    }

    return templates.TemplateResponse('blog/post/post.html', context=context)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        log_level='info',
        reload=True
    )
