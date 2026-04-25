from orders.common.messaging.rabbitmq import EventConsumer
from orders.models import UserSnapshot


class UserEventConsumer(EventConsumer):
    def __init__(self):
        super().__init__(
            queue_name="order_user_events",
            routing_key="user.*"
        )
        print("consumed")


    def handle_event(self, event):
        event_type = event.get("event_type")
        data = event.get("data", {})

        user_id = data.get("user_id")

        if not user_id:
            print("Invalid event: missing user_id")
            return

        if event_type in ["user.created", "user.updated"]:
            UserSnapshot.objects.update_or_create(
                id=user_id,
                defaults={
                    "email": data.get("email"),
                    "first_name": data.get("first_name"),
                    "last_name": data.get("last_name"),
                }
            )

            print(f"User snapshot updated: {user_id}")

        else:
            print(f"Ignored event type: {event_type}")