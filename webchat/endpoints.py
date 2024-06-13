from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from fastapi.requests import Request

from configs import settings

from core import manager

router = APIRouter()

@router.get('/', name='chat')
async def chat_endpoint(request: Request):
    context = {'request': request}
    return settings.TEMPLATES.TemplateResponse('chat/chat.html', context=context)


@router.websocket('/ws/{client_id}')
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(data, client_id)
            await manager.broadcast(f"Client #{client_id} says: {data}", exclude_client_id=client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat.", exclude_client_id=client_id)


@router.websocket('/switch-channel/{client_id}/{new_channel}')
async def switch_channel(websocket: WebSocket, client_id: str, new_channel: str):
    # Disconnect from the current channel
    manager.disconnect(client_id)

    # Connect to the new channel
    await manager.connect(websocket, client_id)

    # Notify the client about the channel switch
    await manager.send_personal_message(f"You have switched to channel {new_channel}", client_id)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(data, client_id)
            await manager.broadcast(f"Client #{client_id} says: {data}", exclude_client_id=client_id)
    except WebSocketDisconnect:
        manager.disconnect(client_id)
        await manager.broadcast(f"Client #{client_id} left the chat.", exclude_client_id=client_id)
