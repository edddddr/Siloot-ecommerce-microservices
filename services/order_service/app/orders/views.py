
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer
from orders.services.cart_client import CartServiceClient
from orders.services.order_creator import create_order_from_cart

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
    
    @action(detail=True, methods=["post"])
    def mark_paid(self, request, pk=None):
        order = self.get_object()
        order.status = "PAID"
        order.save()
        return Response({"status": "PAID"}, status=status.HTTP_200_OK)