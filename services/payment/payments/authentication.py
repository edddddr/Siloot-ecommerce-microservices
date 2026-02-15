from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class JWTAuthWithRole(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Build a simple user object from JWT payload
        """
        user_id = validated_token.get("user_id") or validated_token.get("id")
        role = validated_token.get("role", "customer")  # <-- default customer

        if not user_id:
            raise exceptions.AuthenticationFailed("User not found", code="user_not_found")

        class SimpleUser:
            def __init__(self, id, role):
                self.id = id
                self.role = role
                self.is_authenticated = True

        return SimpleUser(id=user_id, role=role)
