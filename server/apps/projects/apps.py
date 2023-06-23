from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProjectsConfig(AppConfig):
    """Class-configuration of projects app."""

    name = 'apps.projects'
    verbose_name = _("Projects")
