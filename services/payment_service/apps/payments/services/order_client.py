import requests
from django.conf import settings


def mark_order_paid(order_id, token):
    response = requests.post(
        f"{settings.ORDER_SERVICE_URL}/api/orders/{order_id}/mark-paid/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=3,
    )
    response.raise_for_status()