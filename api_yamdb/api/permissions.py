from rest_framework import permissions
from users.models import ADMIN, MODERATOR


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class Moderator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            return user.role in [MODERATOR, ADMIN] or user.is_superuser
        return False


class Administrator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = request.user
            return user.role == ADMIN or user.is_superuser
        return False


class OwnerOrReadOnly(permissions.BasePermission):
    """Only owner, moderator & admins can edit or delete object permission."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.user.role in [MODERATOR, ADMIN]
                or request.user.is_superuser or obj.author == request.user)
