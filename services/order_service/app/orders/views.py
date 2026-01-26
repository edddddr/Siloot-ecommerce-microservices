
from rest_framework import viewsets, permissions, status
from .models import Order
from rest_framework.response import Response
from orders.services.cart_client import CartServiceClient
from orders.services.order_creator import create_order_from_cart
from .serializers import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        token = request.auth
        cart_client = CartServiceClient(token=str(token))

        cart_data = cart_client.get_cart()

        order = create_order_from_cart(
            user_id=request.user.id,
            cart_data=cart_data
        )

        cart_client.clear_cart()

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)