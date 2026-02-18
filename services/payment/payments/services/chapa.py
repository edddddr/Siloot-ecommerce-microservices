import requests
from django.conf import settings


def chapa_initialize_payment(amount, email, full_name, tx_ref, callback_url):
    url = f"{settings.CHAPA_BASE_URL}/transaction/initialize"

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "amount": str(amount),
        "currency": "ETB",
        "email": email,
        "first_name": full_name,
        "tx_ref": tx_ref,
        "callback_url": callback_url,
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


def chapa_verify_payment(tx_ref):
    url = f"{settings.CHAPA_BASE_URL}/transaction/verify/{tx_ref}"

    headers = {
        "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
    }

    response = requests.get(url, headers=headers)
    return response.json()