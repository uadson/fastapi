from fastapi import FastAPI

from core.configs import settings

from api.v1.api import api_router

app = FastAPI(
    title="Security API - FastAPI SQL Alchemy"
)
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True
    )

"""
Token:
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0eXBlIjoiYWNjZXNzX3Rva2VuIiwiZXhwIjoxNjgxMTUwNTc2LCJpYXQiOjE2ODA1NDU3NzYsInN1YiI6IjQifQ.whs6qpy_9dh_CQ6uS5nRRpgyd0bA10HxQAGTkr_XKn8

Tipo:
bearer
"""