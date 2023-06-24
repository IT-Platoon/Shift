from typing import Any

from django.contrib.auth.models import User
from django.db import models

from apps.core.serializers import BaseModelSerializer, serializers
from apps.projects.models import Project, Task


class ProjectSerializer(BaseModelSerializer):
    """Serializer for Project model."""

    owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
    )

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "owner",
        )

    def to_representation(self, instance: Any) -> Any:
        data = super().to_representation(instance)
        data["consists"] = self._user in instance.members.all()
        data["send_request"] = self._user in instance.want_to_enter.all()
        return data


class Actions(models.TextChoices):
    ADD = "ADD", "Add user to project"
    REMOVE = "REMOVE", "Remove user from project"
    REMOVE_WANT_ENTER = "REMOVE_WANT_ENTER", "Remove user from want-to-enter list"


class ProjectMemberSerializer(serializers.Serializer):
    """Serializer for pair project and feature member."""

    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )
    project = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.all(),
    )
    action = serializers.ChoiceField(
        choices=Actions.choices,
    )

    def validate(self, attrs: Any) -> Any:
        validated_data = super().validate(attrs)
        user = validated_data["user"]
        project = validated_data["project"]
        action = validated_data["action"]

        match action:
            case Actions.ADD:
                if user in project.members.all():
                    raise serializers.ValidationError(
                        "User already in project",
                    )
                if user not in project.want_to_enter.all():
                    raise serializers.ValidationError(
                        "User not in list of want to enter of project",
                    )
            case Actions.REMOVE:
                if user not in project.members.all():
                    raise serializers.ValidationError(
                        "User is not member of project",
                    )
            case Actions.REMOVE_WANT_ENTER:
                if user not in project.want_to_enter.all():
                    raise serializers.ValidationError(
                        "User not in list of want to enter of project",
                    )
        return validated_data


class TaskSerializer(BaseModelSerializer):

    class Meta:
        model = Task
        fields = (
            "code",
            "name",
        )
