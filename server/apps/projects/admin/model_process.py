from django.contrib import admin

from apps.projects.models import ModelProcess, ModelGraphics


@admin.register(ModelProcess)
class ModelProcessAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request_file",
        "project",
    )


@admin.register(ModelGraphics)
class ModelGraphicsAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "model",
        "graphic",
    )