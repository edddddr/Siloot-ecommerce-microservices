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
    user_id = request.user_data["id"]

    cart = add_item(
        user_id,
        request.data["product_id"],
        request.data["quantity"]
    )

    return Response(cart)


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