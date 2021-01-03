from rest_framework import permissions
from .models import Role, User


# разрешения для ревью и комментов
class IsAuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            obj.author == request.user or
            request.user.role == Role.ADMIN or
            request.user.role == Role.MODERATOR
        )


# разрешения для жанров и категорий
class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_superuser
        )


# разрешения для users/
class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.ADMIN or request.user.is_superuser
