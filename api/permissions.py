from rest_framework.permissions import BasePermission, SAFE_METHODS


class ForReadOnly(BasePermission):  # рарешение только для безопасных операций

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # проверяю разрешения: только безопасные операции
        # или авторизованный владелец сайта (админ)
        return (
            request.method in SAFE_METHODS or
            request.user and request.user.is_staff  # is_staff
            and request.user.is_authenticated
        )

class IsAuthorOrReadOnlyPermission(BasePermission):

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
        )

class IsSuperuserPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser 
