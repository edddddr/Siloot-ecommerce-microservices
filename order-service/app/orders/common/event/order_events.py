import uuid
from datetime import datetime
from orders.models import UserSnapshot

def build_order_created_event(order):
    user = UserSnapshot.objects.get(id=order.user_id)
    print("-- - -- - - user", 
        "email", user.email,
        "first_name", user.first_name,
        "last_name", user.last_name,
          )


    return {
        "event_id": str(uuid.uuid4()),
        "event_type": "order.created",
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "order_id": str(order.id),
            "user_id": str(order.user_id),
            "amount": str(order.total_amount),
            "currency": order.currency,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }