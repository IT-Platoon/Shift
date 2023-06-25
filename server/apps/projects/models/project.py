from django.contrib.auth.models import User
from django.db import models


class Project(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name="Name project",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name="Owner of project",
    )
    want_to_enter = models.ManyToManyField(
        User,
        related_name="want_to_enter",
        verbose_name="List users, that want to enter to project",
    )
    members = models.ManyToManyField(
        User,
        related_name="projects_member",
        verbose_name="List users, that consist in project",
    )

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"

    def __str__(self) -> str:
        return f"Project {self.name}"
