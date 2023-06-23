from rest_framework import permissions


class ModelProcessPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            return request.user in obj.members.all()
        return False
