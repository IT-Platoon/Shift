from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from apps.core.viewsets import CreateRetrieveViewSet
from apps.projects.models import ModelProcess
from apps.projects.permissions import ModelProcessPermission
from apps.projects.serializers import (
    ModelProcessSerializer,
)
from apps.projects.tasks import model_predict


class ModelProcessViewSet(CreateRetrieveViewSet):
    serializer_class = ModelProcessSerializer
    permission_classes = (IsAuthenticated, ModelProcessPermission)

    def create(self, request, *args, **kwargs):
        serializer = ModelProcessSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        models_process = ModelProcess.objects.get(pk=serializer.data["id"])
        model_predict.delay(models_process.id, request.user.email)
        model_process_serializer = ModelProcessSerializer(
            models_process,
            context={"request": request},
        ).data
        response = {
            "model_process": model_process_serializer,
            "message": "Данные загружены. Ожидайте результатов.",
        }
        return Response(
            data=response,
            status=status.HTTP_201_CREATED,
        )
