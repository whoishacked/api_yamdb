from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from titles.models import Category, Genre, Titles
from .serializers import CategorySerializer, GenreSerializer, TitleSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year')
