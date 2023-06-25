from typing import Any

from apps.core.serializers import BaseModelSerializer, serializers
from apps.projects.models import ModelProcess, Project


class ModelProcessSerializer(BaseModelSerializer):
    """Serializer for ModelProcess model."""

    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )

    class Meta:
        model = ModelProcess
        fields = (
            "id",
            "request_file",
            "project",
        )
    
    def validate_request_file(self, request_file):
        if not request_file:
            raise serializers.ValidationError(
                "Файл не загружен",
            )
        if request_file.name.split('.')[-1] not in ('csv', 'xlsx'):
            raise serializers.ValidationError(
                "Файл должен иметь расширение .xlsx или .csv",
            )
        return request_file

    def validate_project(self, project):
        if self._user not in project.members.all():
            raise serializers.ValidationError(
                "Пользователь не состоит в группе",
            )
        return project

    def to_representation(self, instance: Any) -> dict:
        data = super().to_representation(instance)
        created_date = instance.created.date()
        created_time = instance.created.time().replace(microsecond=0)
        data["created"] = f"{created_date} {created_time}"
        data["graphic"] = instance.graphic
        return data
