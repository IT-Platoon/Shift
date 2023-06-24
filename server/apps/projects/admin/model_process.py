from django.contrib import admin

from apps.projects.models import ModelProcess


@admin.register(ModelProcess)
class ModelProcessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request_file",
        "project",
        "graphic",
    )
