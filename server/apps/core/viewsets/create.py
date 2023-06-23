from rest_framework import mixins, viewsets


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """CreateViewSet for `create`."""
