from orders.models import Order, OrderItem


def create_order_from_cart(user_id, cart_data):
    if not cart_data["items"]:
        raise ValueError("Cart is empty")

    order = Order.objects.create(
        user_id=user_id,
        total_amount=cart_data["total_amount"],
    )

    for item in cart_data["items"]:
        OrderItem.objects.create(
            order=order,
            product_id=item["product_id"],
            quantity=item["quantity"],
            price=item["price"],
        )

    return order