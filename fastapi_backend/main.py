from fastapi import FastAPI , Depends
from typing import Annotated
from schemas import TokenData
from consumer import RabbitMQConsumer
import threading
from oauth2 import verify_access_token

app = FastAPI()
consumer = RabbitMQConsumer()

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

