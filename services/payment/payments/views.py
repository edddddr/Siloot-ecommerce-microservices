import requests
import uuid

from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .tasks import process_payment_task

from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Payment.objects.all()
        return Payment.objects.filter(user_id=user.id)

    def perform_create(self, serializer):
        idempotency_key = self.request.headers.get("Idempotency-Key")

        if idempotency_key:
            existing = Payment.objects.filter(idempotency_key=idempotency_key).first()
            if existing:
                raise ValidationError("Duplicate request detected.")

        serializer.save(
            user_id=self.request.user.id,
            idempotency_key=idempotency_key
        )
    
    

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        payment = self.get_object()

        if payment.status != "pending":
            raise ValidationError("Payment already processed.")
        
        process_payment_task.delay(payment.id, request.headers.get("Authorization"))

        return Response({"message": "Payment is being processed"})
    

    
@api_view(["POST"])
@permission_classes([AllowAny])
def payment_webhook(request):
    payment_id = request.data.get("payment_id")
    status = request.data.get("status")

    try:
        payment = Payment.objects.get(id=payment_id)

        if payment.status != "successful":
            payment.status = status
            payment.save()

        return Response({"message": "Webhook processed"})
    except Payment.DoesNotExist:
        return Response({"error": "Payment not found"}, status=404)