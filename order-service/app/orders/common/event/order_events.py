import uuid
from datetime import datetime

def build_order_created_event(order):
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "order.created",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "order_id": str(order.id),
            "user_id": str(order.user_id),
            "amount": str(order.total_amount),
            "currency": order.currency,
        }
    }