<<<<<<< HEAD
=======
import requests
import uuid

>>>>>>> b3e5504540a0b6e53f893705354447de26d41d17
from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

<<<<<<< HEAD
from .tasks import update_order_status_task
import stripe
=======
from .tasks import process_payment_task
>>>>>>> b3e5504540a0b6e53f893705354447de26d41d17

from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

<<<<<<< HEAD
stripe.api_key = settings.STRIPE_SECRET_KEY
=======
>>>>>>> b3e5504540a0b6e53f893705354447de26d41d17

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
<<<<<<< HEAD

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": payment.currency.lower(),
                    "product_data": {
                        "name": f"Order {payment.order_id}",
                    },
                    "unit_amount": int(payment.amount * 100),
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="http://localhost:3000/success",
            cancel_url="http://localhost:3000/cancel",
            metadata={
                "payment_id": payment.id
            }
        )

        return Response({
            "checkout_url": checkout_session.url
        })

=======
        
        process_payment_task.delay(payment.id, request.headers.get("Authorization"))

        return Response({"message": "Payment is being processed"})
>>>>>>> b3e5504540a0b6e53f893705354447de26d41d17
    

    
@api_view(["POST"])
@permission_classes([AllowAny])
<<<<<<< HEAD
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return Response(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        payment_id = session["metadata"]["payment_id"]

        payment = Payment.objects.get(id=payment_id)

        payment.status = "successful"
        payment.transaction_id = session["payment_intent"]
        payment.save()

        update_order_status_task.delay(payment.id)

    return Response(status=200)
=======
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
>>>>>>> b3e5504540a0b6e53f893705354447de26d41d17
