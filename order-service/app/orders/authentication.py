import jwt
import os

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


PUBLIC_KEY = os.getenv("AUTH_PUBLIC_KEY")


class InternalServiceAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise AuthenticationFailed("Authorization header missing")

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(
                token,
                PUBLIC_KEY,
                algorithms=["RS256"],
                audience="internal_services"
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")

        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        if payload.get("role") != "internal_service":
            raise AuthenticationFailed("Invalid service token")

        return (payload, None)