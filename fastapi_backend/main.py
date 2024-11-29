from fastapi import FastAPI
from consumer import RabbitMQConsumer
import threading

app = FastAPI()
consumer = RabbitMQConsumer()

@app.on_event("startup")
async def startup_event():
    consumer_thread = threading.Thread(target=consumer.start_consuming)
    consumer_thread.start()

@app.on_event("shutdown")
async def shutdown_event():
    consumer.close() 