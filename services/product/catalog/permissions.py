from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrSeller(BasePermission):
    def has_permission(self, request, view):
        # Read-only allowed for anyone
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        # Make sure role is string and lowercase
        role = getattr(user, "role", "").lower()
        return role in ["admin", "seller"]
