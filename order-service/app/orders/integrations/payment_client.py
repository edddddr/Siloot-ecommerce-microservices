import requests
import os
from .auth_client import AuthClient

PAYMENT_SERVICE_URL = os.getenv("PAYMENT_SERVICE_URL")


class PaymentClient:

    @staticmethod
    def start_payment(payload):
        token = AuthClient.get_internal_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        

        response = requests.post(
            PAYMENT_SERVICE_URL,
            json=payload,
            headers=headers
        )

        if response.status_code not in [200, 201]:
            raise Exception("Payment initiation failed")

        return response.json()