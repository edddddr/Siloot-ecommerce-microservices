import json
from payments.common.messaging.rabbitmq import EventConsumer

class OrderCreatedConsumer(EventConsumer):
    def __init__(self):
        super().__init__(
            queue_name="payment_order_created",
            routing_key="order.created"
        )

    def handle(self, event):
        print("[Payment] Processing order:", event["data"]["order_id"])

        # Simulate payment processing
        # order_id = event["data"]["order_id"]
        # amount = event["data"]["amount"]
        order_id = "123"

        amount = 200
    
        # TODO: real payment logic
        success = True

        if success:
            from payments.events import publish_payment_completed
            publish_payment_completed(order_id, amount)

