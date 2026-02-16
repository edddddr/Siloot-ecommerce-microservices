import time
import uuid
import requests
from celery import shared_task
from django.conf import settings
from .models import Payment


@shared_task
def process_payment_task(payment_id, auth_header):
    time.sleep(5)  # simulate provider delay

    payment = Payment.objects.get(id=payment_id)

    payment.status = "successful"
    payment.transaction_id = str(uuid.uuid4())
    payment.save()

    # Update order service
    try:
        requests.patch(
            f"{settings.ORDER_SERVICE_URL}{payment.order_id}/",
            json={"status": "processing"},
            headers={"Authorization": auth_header},
        )
    except Exception:
        pass
