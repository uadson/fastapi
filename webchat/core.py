from fastapi import WebSocket


class ConnectionManager:
    def __init__(self):
        self.active_connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket

    def disconnect(self, client_id: str):
        del self.active_connections[client_id]

    async def send_personal_message(self, message: str, client_id: str):
        websocket = self.active_connections.get(client_id)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str, exclude_client_id: str = None):
        for client_id, websocket in self.active_connections.items():
            if client_id != exclude_client_id:
                await websocket.send_text(message)

manager = ConnectionManager()
