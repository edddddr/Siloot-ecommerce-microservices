import requests
from django.conf import settings


class InventoryClient:

    @staticmethod
    def get_stock(product_id):

        url = f"{settings.INVENTORY_SERVICE_URL}/api/v1/inventory/stock/{product_id}/"


        response = requests.get(url)

        if response.status_code != 200:
            raise Exception("Inventory service unavailable")

        data = response.json()
        

        return data["available_stock"]