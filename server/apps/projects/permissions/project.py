from rest_framework import permissions


class ProjectPermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj) -> bool:
        if request.method == "GET":
            return request.user in obj.members.all()
        if request.method in ("DELETE", "PATCH"):
            return request.user.id == obj.owner.id
        return False
