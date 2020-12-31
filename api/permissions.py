from rest_framework import permissions
from .models import Role

# из пермишенов для части 'part_c' нужен только ReviewAndCommentPermission
# остальные можно подчистить если они не нужны вам
class ReviewAndCommentPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS or (
            request.user == obj.author or
            request.user.role == 'admin' or
            request.user.role == 'moderator'
        )


class IsAuthorOrReadOnlyPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


# этот пермишен для жанров и категорий
class AdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS or
            request.user and request.user.is_staff
            and request.user.is_authenticated
        )

class ModeratorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self,request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author != request.user)


class AdminPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == Role.ADMIN or request.user.is_superuser
