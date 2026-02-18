from django.conf import settings
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .tasks import update_order_status_task
import stripe

from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

stripe.api_key = settings.STRIPE_SECRET_KEY

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

    

    
@api_view(["POST"])
@permission_classes([AllowAny])
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
