from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/')
async def index():
    context = """
        <center>
            <h1>FastAPI Web na <u>Geek University</u></h1>
            <span>Para mais cursos, visite nosso site clicando <a href="https://www.geekuniversity.com.br" target="_blank">aqui</a></span>
        </center>    
    """
    return HTMLResponse(content=context)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="main:app",
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
