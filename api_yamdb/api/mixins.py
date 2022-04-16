from rest_framework import viewsets, mixins


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    class Meta:
        abstract = True


class CreateListDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    """
    Базовый вьюсет для категорий и жанров.
    """
    pass
