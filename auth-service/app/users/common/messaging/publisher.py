import json
from .rabbitmq import RabbitMQConnection


class EventPublisher:
    def __init__(self, exchange="events"):
        self.exchange = exchange
        self.connection = RabbitMQConnection()
        self.channel = self.connection.channel

        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type="topic",
            durable=True
        )

    def publish(self, routing_key: str, event: dict):
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=json.dumps(event),
            properties=None
        )

    def close(self):
        self.connection.close()