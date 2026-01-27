import requests
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def get_user_from_auth_service(token: str):
    try:
        # 1. Use the internal Docker service name (e.g., http://auth_service:8000)
        response = requests.get(
            f"{settings.AUTH_SERVICE_URL}/api/auth/me/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=3,
        )

        if response.status_code != 200:
            raise AuthenticationFailed("Invalid token")

        return response.json()

    # 2. PLACE THE NEW BLOCK HERE:
    except requests.RequestException as e:
        # This prints to your terminal/docker logs for YOU to see
        print(f"DEBUG: Auth Service Connection Error: {e}") 
        
        # This sends a more helpful message back to the API client (Postman)
        raise AuthenticationFailed(f"Auth service unreachable at {settings.AUTH_SERVICE_URL}. Error: {e}")