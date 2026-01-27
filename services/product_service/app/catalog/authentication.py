from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .services.auth_client import get_user_from_auth_service


class AuthServiceAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth = request.headers.get("Authorization")
        if not auth or not auth.startswith("Bearer "):
            return None

        token = auth.split(" ")[1]
        user_data = get_user_from_auth_service(token)

        # lightweight user object (NO DB HIT)
        class ServiceUser:
            def __init__(self, user):
                self.id = user["id"]
                self.email = user.get("email")
                self.is_authenticated = True

        return ServiceUser(user_data), None