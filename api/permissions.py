from rest_framework import permissions
from .models import Role


# разрешения для ревью и комментов
class ReviewAndCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user == obj.author or
            request.user.role == 'admin' or
            request.user.role == 'moderator'
        )


# разрешения для жанров и категорий
class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
            and request.user.is_authenticated
        )


# разрешения для users/
class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.ADMIN or request.user.is_superuser
