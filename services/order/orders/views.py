from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from .models import Order
from .serializers import OrderSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # customer_id comes from JWT
        serializer.save(customer_id=self.request.user.id)

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Order.objects.all()
        return Order.objects.filter(customer_id=user.id)
    
    @action(detail=True, methods=["patch"], permission_classes=[permissions.AllowAny])
    def update_status(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        order.status = request.data.get("status")
        order.save()
        return Response({"status": "updated"})
