from fastapi import WebSocket
from fastapi.routing import APIRouter

from controller.departments import departments_list

from core.configs import settings

router = APIRouter()

@router.websocket('/')
async def chat(websocket: WebSocket):
    departments = departments_list(settings.URL_DEPARTMENTS)
    
    await websocket.accept()
    
    while True:
        user_input = await websocket.receive_text()
        await websocket.send_json({'user': user_input})
