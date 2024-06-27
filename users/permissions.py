from rest_framework import permissions


class IsModerators(permissions.BasePermission):
    """Проверка на модератора"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверка на владельца"""

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False


class IsUser(permissions.BasePermission):
    """Проверка на пользователя"""

    def has_object_permission(self, request, view, obj):
        if obj.email == request.user.email:
            return True
        return False
