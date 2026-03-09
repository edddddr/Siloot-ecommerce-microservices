from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import CartItem
from .serializers import (
    CartSerializer,
    AddItemSerializer,
    UpdateItemSerializer,
)

from .services import CartService


class CartView(APIView):

    def get(self, request):

        user_id = request.headers.get("X-User-ID")

        cart = CartService.get_or_create_cart(user_id)

        serializer = CartSerializer(cart)

        return Response(serializer.data)


class AddItemView(APIView):

    def post(self, request):

        user_id = request.headers.get("X-User-ID")

        serializer = AddItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = CartService.add_item(
            user_id=user_id,
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )

        return Response(
            {"item_id": item.id},
            status=status.HTTP_201_CREATED
        )


class UpdateItemView(APIView):

    def patch(self, request, item_id):

        serializer = UpdateItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        item = CartService.update_item(
            cart_item_id=item_id,
            quantity=serializer.validated_data["quantity"],
        )

        return Response({"item_id": item.id})


class RemoveItemView(APIView):

    def delete(self, request, item_id):

        CartService.remove_item(item_id)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ClearCartView(APIView):

    def delete(self, request):

        user_id = request.headers.get("X-User-ID")

        CartService.clear_cart(user_id)

        return Response(status=status.HTTP_204_NO_CONTENT)