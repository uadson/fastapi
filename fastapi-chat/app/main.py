import uvicorn

from fastapi import FastAPI

from views import chat

app = FastAPI(docs_url=None, redoc_url=None)
app.include_router(chat.router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8002,
        log_level="info",
    )