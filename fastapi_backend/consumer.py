import pika
import json


class RabbitMQConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        
        # Declare each queue explicitly
        self.channel.queue_declare(queue='user_creation')
        self.channel.queue_declare(queue='order_creation')

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        print(f"Received message: {message}")

    def start_consuming(self):
        # Set up consumers for each queue
        self.channel.basic_consume(queue='user_creation', on_message_callback=self.callback, auto_ack=True)
        self.channel.basic_consume(queue='order_creation', on_message_callback=self.callback, auto_ack=True)

        print("Waiting for messages in user_creation and order_creation.")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()