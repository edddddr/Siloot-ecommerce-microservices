import logging
import requests
from django.conf import settings

from requests.exceptions import RequestException, Timeout

from cart.exceptions import ProductNotFoundError


logger = logging.getLogger(__name__)


class ProductClient:

    @staticmethod
    def get_product(product_id):


        url = f"{settings.PRODUCT_SERVICE_URL}/api/v1/products/{product_id}/"

        try:
            
            response = requests.get(url, timeout=(2.0, 5.0))
            # print("\n", "response : ", response, "\n" )
            if response.status_code == 404:
                logger.warning("Product not found in Product Service", extra={"product_id": product_id})
                return None
                

            if response.status_code != 200:
                logger.error(
                    "Product Service returned an error", 
                    extra={"status_code": response.status_code, "product_id": product_id}
                )
                return None

            
            logger.debug("Successfully fetched product details", extra={"product_id": product_id})
            return response.json()

        except Timeout:
            # 4. Specific Timeout handling
            logger.critical(
                "Product Service timed out", 
                extra={"product_id": product_id, "url": url}
            )
            return None

        except RequestException as e:
            # 5. General Network/Connection issues
            logger.error(
                "Network error connecting to Product Service", 
                extra={"error": str(e), "product_id": product_id}
            )
            return None
        
        except Exception as e:
            logger.error("Unexpected error in ProductClient", extra={"error": str(e)}, exc_info=True)
            return None