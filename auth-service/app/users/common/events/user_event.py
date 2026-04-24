import uuid
from datetime import datetime


def build_user_event(user, event_type: str):
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.utcnow().isoformat(),
        "data": {
            "user_id": str(user.id),
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
    }