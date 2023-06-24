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


class Task(models.Model):
    code = models.CharField(
        max_length=16,
        verbose_name="Код задачи",
    )
    name = models.CharField(
        max_length=256,
        verbose_name="Код задачи",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self) -> str:
        return f"Task {self.code} {self.name}"
