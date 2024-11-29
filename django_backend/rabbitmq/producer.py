import pika
import json
import logging

class RabbitMQPublisher:
    def __init__(self):
        self.connection = None
        self.channel = None

    def connect(self):
        if self.connection is None or not self.connection.is_open:
            try:
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
                self.channel = self.connection.channel()
                logging.info("Connected to RabbitMQ")
            except pika.exceptions.AMQPConnectionError as e:
                logging.error(f"Could not connect to RabbitMQ: {e}")

    def publish_event(self, message, queue_name):
        self.connect()  # Connect when publishing

        if not self.channel:
            logging.warning("Not connected to RabbitMQ, cannot publish message.")
            return

        try:
            # Declare the queue
            self.channel.queue_declare(queue=queue_name)

            # Publish the message
            self.channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=json.dumps(message)  # Convert the message to JSON
            )
            logging.info(f"Published message to {queue_name}: {message}")

        except Exception as e:
            logging.error(f"Failed to publish message to {queue_name}: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            logging.info("Connection to RabbitMQ closed.")

# Usage
publisher = RabbitMQPublisher()