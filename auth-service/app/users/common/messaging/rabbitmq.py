import pika
import json
from django.conf import settings


class RabbitMQConnection:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.URLParameters(settings.RABBITMQ_URL)
        )
        self.channel = self.connection.channel()

    def close(self):
        self.connection.close()