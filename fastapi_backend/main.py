from fastapi import FastAPI , Depends, HTTPException, WebSocket, WebSocketDisconnect, Request
from oauth2 import verify_access_token, oauth2_scheme
from websocket import ConnectionManager
from fastapi.templating import Jinja2Templates
from consumer import RabbitMQConsumer
from permitions import verify_permission
import threading


app = FastAPI()
consumer = RabbitMQConsumer()
manager = ConnectionManager()
templates = Jinja2Templates(directory="templates")






@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=consumer.start_consuming)
    consumer_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    consumer.close() 


@app.get("/")
def get_user(user_id: int = Depends(verify_access_token)):
    return {"user_id": user_id}

@app.get("/class/{course_id}")
def get_class( request: Request, course_id: int, token: str = Depends(oauth2_scheme) ,user_id: int = Depends(verify_access_token), permission: bool = Depends(verify_permission)):

    return templates.TemplateResponse("chatroom.html", {"request": request, "course_id": course_id, "user_id": user_id, "token": token})




@app.websocket("/ws/{course_id}/")
async def websocket_endpoint(course_id: int, websocket: WebSocket):
    # Extract the token from the WebSocket query parameters
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008, reason="Token missing")
        return

    try:
        user_id = verify_access_token(token)
    except HTTPException as e:
        await websocket.close(code=1008, reason=e.detail)
        return
    
    await manager.connect(course_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(course_id, user_id, data)
    except WebSocketDisconnect:
        manager.disconnect(course_id, websocket)
        print(f"User {user_id} disconnected from course {course_id}")