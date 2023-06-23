from django.contrib.auth.models import User
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.viewsets import BaseViewSet
from apps.projects.models import Project
from apps.projects.permissions import ProjectPermission
from apps.projects.serializers import (
    ModelProcessSerializer,
    ProjectMemberSerializer,
    ProjectSerializer,
)
from apps.users.serializers import UserSerializer


class ProjectViewSet(BaseViewSet):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, ProjectPermission)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("name",)

    def get_queryset(self) -> QuerySet:
        return Project.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        project = Project.objects.prefetch_related("members").get(
            pk=serializer.data["id"],
        )
        project.members.add(request.user)
        project_serializer = ProjectSerializer(
            project,
            context={"request": request},
        ).data
        response = {
            "project": project_serializer,
            "message": "Проект успешно создан.",
        }
        return Response(
            data=response,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(methods=("GET",), detail=True, url_path="get-want-enter")
    def get_want_to_enter(self, request, pk) -> Response:
        if not request.user.is_authenticated:
            return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
        project = get_object_or_404(
            Project.objects.select_related(
                "owner",
            ).prefetch_related(
                "want_to_enter",
            ),
            id=pk,
        )
        if request.user.id != project.owner.id:
            message = "Только владелец может увидеть тех, кто хочет вступить."
            return Response(
                data={"message": message},
                status=status.HTTP_403_FORBIDDEN,
            )
        user_serializer = UserSerializer(
            project.want_to_enter.all(),
            many=True,
        ).data
        return Response(
            data=user_serializer,
            status=status.HTTP_200_OK,
        )

    @action(methods=("GET",), detail=True, url_path="get-members")
    def get_members(self, request, pk) -> Response:
        if not request.user.is_authenticated:
            return Response(
            status=status.HTTP_401_UNAUTHORIZED,
        )
        project = get_object_or_404(
            Project.objects.prefetch_related("members"),
            id=pk,
        )
        user_serializer = UserSerializer(
            project.members.all(),
            many=True,
        ).data
        return Response(
            data=user_serializer,
            status=status.HTTP_200_OK,
        )

    @action(methods=("POST",), detail=True, url_path="want-enter")
    def add_to_want_to_enter(self, request, pk) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        project = get_object_or_404(
            Project.objects.prefetch_related("members", "want_to_enter"),
            id=pk,
        )
        if request.user in project.members.all():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"message": "Вы уже состоите в проекте."},
            )
        project.want_to_enter.add(request.user)
        return Response(
            data={"message": "Заявка на вступление в проект отправлена."},
            status=status.HTTP_200_OK,
        )

    @action(methods=("POST",), detail=True, url_path="cancel-want-enter")
    def cancel_want_to_enter(self, request, pk) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        project = get_object_or_404(
            Project.objects.prefetch_related("want_to_enter"),
            id=pk,
        )
        project.want_to_enter.remove(request.user)
        return Response(
            data={"message": "Вы отменили заявку на вступление в проект."},
            status=status.HTTP_200_OK,
        )
    
    @action(methods=("POST",), detail=False, url_path="remove-want-enter")
    def remove_from_want_to_enter(self, request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.select_related(
            "owner",
        ).prefetch_related(
            "want_to_enter",
        ).get(id=serializer.data["project"])
        if request.user.id == project.owner.id:
            user = User.objects.get(id=serializer.data["user"])
            project.want_to_enter.remove(user)
            want_to_enter = UserSerializer(
                project.want_to_enter.all(),
                many=True,
            ).data
            response = {
                "want_to_enter": want_to_enter,
            }
            return Response(
                status=status.HTTP_200_OK,
                data=response,
            )
        message = "Отклонить заявку может только владелец проекта."
        return Response(
            data={"message": message},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(methods=("POST",), detail=False, url_path="add-member")
    def add_to_member(self, request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.select_related(
            "owner",
        ).prefetch_related(
            "want_to_enter", "members",
        ).get(id=serializer.data["project"])
        if request.user.id == project.owner.id:
            user = User.objects.get(id=serializer.data["user"])
            project.want_to_enter.remove(user)
            project.members.add(user)
            want_to_enter = UserSerializer(
                project.want_to_enter.all(),
                many=True,
            ).data
            members = UserSerializer(
                project.members.all(),
                many=True,
            ).data
            response = {
                "want_to_enter": want_to_enter,
                "members": members,
            }
            return Response(
                status=status.HTTP_200_OK,
                data=response,
            )
        return Response(
            data={"message": "Принять заявку может только владелец проекта."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(methods=("POST",), detail=False, url_path="remove-member")
    def remove_from_member(self, request) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        serializer = ProjectMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        project = Project.objects.select_related(
            "owner",
        ).prefetch_related(
            "members",
        ).get(id=serializer.data["project"])
        if request.user.id == project.owner.id:
            user = User.objects.get(id=serializer.data["user"])
            project.members.remove(user)
            members = UserSerializer(project.members.all(), many=True).data
            response = {
                "members": members,
            }
            return Response(
                status=status.HTTP_200_OK,
                data=response,
            )
        message = "Исключить пользователя может только владелец проекта."
        return Response(
            data={"message": message},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(methods=("POST",), detail=True, url_path="leave-project")
    def leave_from_project(self, request, pk) -> Response:
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        project = get_object_or_404(
            Project.objects.select_related(
                "owner",
            ).prefetch_related(
                "members",
            ),
            id=pk,
        )
        if request.user.id != project.owner.id:
            project.members.remove(request.user)
            return Response(
                data={"message": "Вы успешно вышли с проекта."},
                status=status.HTTP_200_OK,
            )
        return Response(
            data={"message": "Владелец не может выйти с проекта."},
            status=status.HTTP_403_FORBIDDEN,
        )

    @action(methods=("GET",), detail=True, url_path="responses")
    def get_responses(self, request, pk, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        project = get_object_or_404(
            Project.objects.prefetch_related("responses", "members"),
            id=pk,
        )
        if request.user not in project.members.all():
            message = (
                "Только участники проекта имеют "
                "доступ к материалам на проекте."
            )
            return Response(
                data={"message": message},
                status=status.HTTP_403_FORBIDDEN,
            )
        responses = ModelProcessSerializer(
            project.responses.order_by("id"),
            many=True,
        ).data
        return Response(
            data=responses,
            status=status.HTTP_200_OK,
        )
