from django.db.models.signals import post_delete
from django.dispatch import receiver

from apps.projects.models import ModelProcess


@receiver(post_delete, sender=ModelProcess)
def delete_request_file_model_process(instance, **kwargs):
    instance.request_file.storage.delete(instance.request_file.path)
