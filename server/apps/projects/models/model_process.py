from django.db import models

from apps.core.models import BaseModel

PATH_REQUEST = "projects/project_{}_{}/request_{}"


def user_directory_path_request(instance, filename) -> str:
    return PATH_REQUEST.format(
        instance.project.id,
        instance.project.name.replace(
            " ", "_",
        ).replace(
            ":", "",
        ).replace(
            "-", "_",
        ),
        filename,
    )


class ModelProcess(BaseModel):
    request_file = models.FileField(
        upload_to=user_directory_path_request,
        verbose_name="Loaded file",
    )
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="Analyzed project",
    )
    graphic = models.JSONField(
        null=True,
        blank=True,
        verbose_name="Model response",
    )

    class Meta:
        verbose_name = "Информация о модели"
        verbose_name_plural = "Информации о моделях"

    def __str__(self) -> str:
        return f"ModelProcess for project {self.project}"
