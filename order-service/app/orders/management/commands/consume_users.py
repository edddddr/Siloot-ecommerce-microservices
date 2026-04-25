# orders/management/commands/consume_users.py

from django.core.management.base import BaseCommand
from orders.consumers.user_consumer import UserEventConsumer


class Command(BaseCommand):
    help = "Consume user events"

    def handle(self, *args, **kwargs):
        consumer = UserEventConsumer()
        consumer.start_consuming(consumer.handle_event)