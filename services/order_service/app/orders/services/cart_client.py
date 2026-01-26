import requests
from django.conf import settings


def get_cart(token: str):
    response = requests.get(
        f"{settings.CART_SERVICE_URL}/api/cart/my/",
        headers={"Authorization": f"Bearer {token}"},
        timeout=3,
    )
    response.raise_for_status()
    return response.json()