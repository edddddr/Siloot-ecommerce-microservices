from rest_framework.permissions import BasePermission


class IsInternalService(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.get("role") == "internal_service"


class IsAdminUserRole(BasePermission):
    def has_permission(self, request, view):
        token = request.auth
        if not token:
            return False
        return token.get("role") == "admin"