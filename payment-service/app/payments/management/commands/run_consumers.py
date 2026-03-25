from django.core.management.base import BaseCommand
from payments.consumers.order_consumer import OrderCreatedConsumer

class Command(BaseCommand):
    help = "Run RabbitMQ consumers"
    print("wainting to ")

    def handle(self, *args, **kwargs):
        consumer = OrderCreatedConsumer()
        consumer.start_consuming(consumer.handle)