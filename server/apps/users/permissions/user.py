from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view,) -> bool:
        return True
