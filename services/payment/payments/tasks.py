import requests
from celery import shared_task
from django.conf import settings
from .models import Payment


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
