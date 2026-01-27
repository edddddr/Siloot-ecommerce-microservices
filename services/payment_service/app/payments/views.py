from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from payments.services.order_client import mark_order_paid


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user_id=self.request.user.id)

    def create(self, request, *args, **kwargs):
        order_id = request.data.get("order_id")
        amount = request.data.get("amount")

        payment = Payment.objects.create(
            order_id=order_id,
            user_id=request.user.id,
            amount=amount,
            status="SUCCESS",  # MVP: assume success
        )

        mark_order_paid(order_id, token=str(request.auth))

        serializer = self.get_serializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    