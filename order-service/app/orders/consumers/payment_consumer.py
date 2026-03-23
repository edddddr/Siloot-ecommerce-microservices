from orders.common.messaging.rabbitmq import EventConsumer
from orders.models import Order
from orders.services import OrderService

class PaymentCompletedConsumer(EventConsumer):
    def __init__(self):
        super().__init__(
            queue_name="order_payment_completed",
            routing_key="payment.completed"
        )
        self.queue_name = "order_payment_completed"

    def handle(self, event):
        data = event["data"]
        order_id = data["order_id"]

        print(f"[Order] Payment completed for order {order_id}")

        try:
            order = Order.objects.get(id=order_id)

            OrderService().update_order_status(
                order,
                new_status="paid",
                note="Payment completed via event"
            )

        except Order.DoesNotExist:
            print(f"[Order] Order not found: {order_id}")


class PaymentFailedConsumer(EventConsumer):
    def __init__(self):
        super().__init__(
            queue_name="order_payment_failed",
            routing_key="payment.failed"
        )
        self.queue_name = "order_payment_failed"

    def handle(self, event):
        data = event["data"]
        order_id = data["order_id"]

        print(f"[Order] Payment failed for order {order_id}")

        try:
            order = Order.objects.get(id=order_id)

            OrderService().update_order_status(
                order,
                new_status="failed",
                note="Payment failed via event"
            )

        except Order.DoesNotExist:
            print(f"[Order] Order not found: {order_id}")