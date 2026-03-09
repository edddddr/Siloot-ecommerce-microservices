import jwt
from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed


class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            raise AuthenticationFailed("Invalid token header")

        try:
            payload = jwt.decode(
                token,
                settings.AUTH_PUBLIC_KEY,
                algorithms=["RS256"],
                audience="cart-service",
            )

        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Token expired")

        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid token")

        user_id = payload.get("user_id")

        if not user_id:
            raise AuthenticationFailed("Invalid token payload")

        return (user_id, None)