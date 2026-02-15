import requests
import uuid

from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .models import Payment
from .serializers import PaymentSerializer


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
        serializer.save(user_id=self.request.user.id)

    @action(detail=True, methods=["post"])
    def process(self, request, pk=None):
        payment = self.get_object()

        if payment.status != "pending":
            raise ValidationError("Payment already processed.")

        # simulate success
        payment.status = "successful"
        payment.transaction_id = str(uuid.uuid4())
        payment.save()

        # 🔥 CALL ORDER SERVICE (internal)
        try:
            response = requests.patch(
                f"{settings.ORDER_SERVICE_URL}{payment.order_id}/update_status/",
                json={"status": "processing"},
                timeout=5,
            )

            print("ORDER SERVICE STATUS:", response.status_code)
            print("ORDER SERVICE RESPONSE:", response.text)

        except Exception as e:
            print("ERROR CALLING ORDER SERVICE:", str(e))

        return Response({"message": "Payment successful"})
