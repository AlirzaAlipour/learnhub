from fastapi import WebSocket




class ConnectionManager:
    def __init__(self):
        # List to hold active connections as tuples of (course_id, websocket)
        self.active_connections = []

    async def connect(self, course_id: int, websocket: WebSocket):
        # Accept the WebSocket connection
        await websocket.accept()
        # Add the connection to the active connections list
        self.active_connections.append((course_id, websocket))

    def disconnect(self, websocket: WebSocket):
        # Remove the connection from the active connections list
        self.active_connections = [
            (cid, ws) for cid, ws in self.active_connections if ws != websocket
        ]

    async def send_message(self, course_id: int, message: str, user_id: str):

        formatted_message = f"{message} : {user_id}"
        # Send a message to all connected users in the specified course
        for cid, websocket in self.active_connections:
            if cid == course_id:
                await websocket.send_text(formatted_message)
