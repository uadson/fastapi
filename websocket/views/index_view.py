import asyncio

from fastapi.routing import APIRouter
from fastapi.requests import Request
from fastapi.websockets import WebSocket
from fastapi.websockets import WebSocketDisconnect

from core.config import settings

router = APIRouter()

@router.get('/')
async def index(request: Request):
    return settings.TEMPLATES.TemplateResponse('index.html', {'request': request})


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("Conexão estabelecida")
    
    async def close_websocket_after_timeout():
        await asyncio.sleep(5)
        await websocket.close()
    
    timeout_task = asyncio.create_task(close_websocket_after_timeout())
    
    try:
        while True:
            data = await websocket.receive_text()
                
            print(f"Dado enviado: {data}")
            await websocket.send_text(data)
            
            timeout_task.cancel()
            timeout_task = asyncio.create_task(close_websocket_after_timeout()) 
            
    except WebSocketDisconnect:
        print("Conexão encerrada")
    finally:
        timeout_task.cancel()
            