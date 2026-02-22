import requests
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .permissions import IsAuthenticatedViaAuthService
from .services import add_item, get_cart, remove_item, clear_cart

@api_view(["GET"])
@permission_classes([IsAuthenticatedViaAuthService])
def view_cart(request):
    user_id = request.user_data["id"]
    return Response(get_cart(user_id))


@api_view(["POST"])
@permission_classes([IsAuthenticatedViaAuthService])
def add_to_cart(request):
    product_id = request.data.get("product_id")
    quantity = request.data.get("quantity")

    # 1️⃣ Call Inventory Service
    try:
        inventory_response = requests.get(
            f"{settings.INVENTORY_SERVICE_URL}/check/",
            params={"product_id": product_id, "quantity": quantity},
            timeout=2
        )
    except requests.exceptions.RequestException:
        return Response(
            {"error": "Stock verification unavailable"},
            status=503
        )

    if inventory_response.status_code != 200:
        return Response({"error": "Inventory error"}, status=400)

    inventory_data = inventory_response.json()

    if not inventory_data["available"]:
        return Response(
            {"error": "Not enough stock"},
            status=400
        )

    # 2️⃣ Save to Cart DB
    # CartItem.objects.create(...)

    return Response({"message": "Item added to cart"})


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedViaAuthService])
def remove_from_cart(request, product_id):
    user_id = request.user_data["id"]
    cart = remove_item(user_id, product_id)
    return Response(cart)


@api_view(["DELETE"])
@permission_classes([IsAuthenticatedViaAuthService])
def clear(request):
    user_id = request.user_data["id"]
    clear_cart(user_id)
    return Response({"message": "Cart cleared"})