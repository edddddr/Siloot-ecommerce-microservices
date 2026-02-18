import requests
from django.conf import settings


def get_user_orders(user_id, auth_header):
    try:
        response = requests.get(
            f"{settings.ORDER_SERVICE_URL}",
            headers={"Authorization": auth_header},
        )
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return []
