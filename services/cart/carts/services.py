import json
import requests
from django.conf import settings
from .redis_client import redis_client

CART_TTL = 60 * 60 * 24 * 7  # 7 days


def get_cart_key(user_id):
    return f"cart:{user_id}"


def get_cart(user_id):
    cart = redis_client.get(get_cart_key(user_id))
    return json.loads(cart) if cart else {"items": []}


def save_cart(user_id, cart):
    redis_client.setex(
        get_cart_key(user_id),
        CART_TTL,
        json.dumps(cart)
    )


def validate_inventory(product_id, quantity):
    response = requests.get(
        f"{settings.INVENTORY_SERVICE_URL}/{product_id}/"
    )

    if response.status_code != 200:
        raise Exception("Product not found")

    data = response.json()

    if data["available_quantity"] < quantity:
        raise Exception("Insufficient stock")

    return True


def add_item(user_id, product_id, quantity):
    validate_inventory(product_id, quantity)

    cart = get_cart(user_id)

    for item in cart["items"]:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            save_cart(user_id, cart)
            return cart

    cart["items"].append({
        "product_id": product_id,
        "quantity": quantity
    })

    save_cart(user_id, cart)
    return cart


def remove_item(user_id, product_id):
    cart = get_cart(user_id)
    cart["items"] = [
        item for item in cart["items"]
        if item["product_id"] != product_id
    ]
    save_cart(user_id, cart)
    return cart


def clear_cart(user_id):
    redis_client.delete(get_cart_key(user_id))