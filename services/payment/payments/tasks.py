import requests
from celery import shared_task
from django.conf import settings
from .models import Payment

from .services.chapa import chapa_verify_payment



@shared_task(bind=True, max_retries=3)
def update_order_status_task(self, payment_id):
    try:
        payment = Payment.objects.get(id=payment_id)

        requests.patch(
            f"{settings.ORDER_SERVICE_URL}{payment.order_id}/",
            json={"status": "processing"},
            timeout=5,
        )

    except Exception as exc:
        # Retry if order service is temporarily down
        raise self.retry(exc=exc, countdown=5)


@shared_task
def verify_payment_task(tx_ref):
    try:
        payment = Payment.objects.get(transaction_id=tx_ref)

        chapa_response = chapa_verify_payment(tx_ref)

        status = chapa_response.get("data", {}).get("status")

        if status == "success":
            payment.status = "completed"
            payment.save()

            # OPTIONAL: notify order service here

        else:
            payment.status = "failed"
            payment.save()

    except Payment.DoesNotExist:
        pass
