import requests
from django.conf import settings


class ProductClient:

    @staticmethod
    def get_product(product_id):

        url = f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{product_id}/"

        response = requests.get(url)
        # print("\n", "response : ", response, "\n" )

        if response.status_code != 200:
            return None
        
        print(response.json())

        return response.json()