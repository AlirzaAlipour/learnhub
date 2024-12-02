import json
import pika
from utils import add_enrollments

class RabbitMQConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='order_creation')

    def callback(self, ch, method, properties, body):
        message = json.loads(body)
        print(f"Received message: {message}")

        user_id = message['user_id']
        course_ids = message['course_ids']

        # Call the add_enrollments service function
        add_enrollments(user_id, course_ids)

    def start_consuming(self):
        self.channel.basic_consume(queue='order_creation', on_message_callback=self.callback, auto_ack=True)
        print("Waiting for messages in order_creation.")
        self.channel.start_consuming()

    def close(self):
        self.connection.close()
