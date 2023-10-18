import uvicorn

from fastapi import FastAPI

from views import index_view

app = FastAPI()

app.include_router(index_view.router)

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        reload=True,
        port=8000,
        log_level="info"
    )
