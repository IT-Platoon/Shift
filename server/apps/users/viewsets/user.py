from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.core.viewsets import CreateViewSet
from apps.users.permissions import UserPermission
from apps.projects.serializers import ProjectSerializer
from apps.users.serializers import UserSerializer


class UserViewSet(CreateViewSet):
    serializer_class = UserSerializer
    permission_classes = (UserPermission,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    @action(methods=("GET",), detail=False)
    def me(self, request):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        return Response(
            data=UserSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    @action(methods=("GET",), detail=False, url_path="projects")
    def projects(self, request):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        projects = request.user.projects_member.all()
        project_serializer = ProjectSerializer(
            projects,
            many=True,
            context={"request": request},
        ).data
        return Response(
            data=project_serializer,
            status=status.HTTP_200_OK,
        )
