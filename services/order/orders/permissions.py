from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrSeller(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        user = request.user
        return user and getattr(user, "role", None) in ["admin", "seller"]
