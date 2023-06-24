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

    def retrieve(self, request, *args, **kwargs):
        model_process = get_object_or_404(
            ModelProcess,
            id=self.kwargs["pk"],
        )
        path_to_file = "media/" + model_process.request_file.name
        with open(path_to_file) as file_obj:
            filename = file_obj.name[file_obj.name.rfind("/")+1:]
            file_to_send = ContentFile(file_obj.read())
            response = HttpResponse(file_to_send, 'application/x-gzip')
            response['Content-Length'] = file_to_send.size
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}"'
            )
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            return response
