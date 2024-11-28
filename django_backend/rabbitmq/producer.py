import pika
import json

class RabbitMQPublisher:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()

    def publish_event(self, message, queue_name):
        # Declare the queue
        self.channel.queue_declare(queue=queue_name)

        # Publish the message
        self.channel.basic_publish(
            exchange='',
            routing_key=queue_name,
            body=json.dumps(message)  # Convert the message to JSON
        )

        print(f"Published message to {queue_name}: {message}")

    def close(self):
        self.connection.close()

