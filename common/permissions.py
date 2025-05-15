from rest_framework import permissions

from apps.core.models import User


class IsAdminUser(permissions.BasePermission):
    """Admin user permission."""

    def has_permission(self, request, view):
        """Return True if the user is an Administrator."""
        return request.user.is_authenticated and request.user.is_superuser


def user_is_management(user: User) -> bool:
    """Return True if the user is a system administrator."""
    return user.is_authenticated and user.is_management
