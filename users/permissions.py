from rest_framework import permissions


class IsModerators(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderators').exists()
