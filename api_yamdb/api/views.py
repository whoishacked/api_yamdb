from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import get_object_or_404
from rest_framework import viewsets, filters, views, status, mixins
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from django.core.mail import EmailMessage

from reviews.models import Category, Genre, Title, Review
from users.models import User
from .serializers import (CategorySerializer, GenreSerializer, TitleSerializer,
                          TitlePostPatchSerializer, UserSerializer,
                          ReviewSerializer, UserRegSerializer,
                          CommentSerializer)
from .mixins import CreateViewSet


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')
    pagination_class = LimitOffsetPagination
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlePostPatchSerializer
        return TitleSerializer 

      
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'


class ReviewViewSet(viewsets.ModelViewSet):
    """Reviews."""
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Comments."""
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['id'])
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['id'])
        serializer.save(author=self.request.user, review=review)


class UserRegViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    lookup_field = 'username'

    def perform_create(self, serializer):
        serializer.save()
        username = serializer.data.get('username')
        user = User.objects.get(username=username)
        print(user.confirmation_code)


class RegAPIView(views.APIView):

    def post(self, request):
        username = request.data.get('username', [])
        if username:
            user = get_object_or_404(User, username=username)
            token = RefreshToken.for_user(user).access_token
            return Response({"token": str(token)}, status=status.HTTP_200_OK)
        else:
            return Response({"field_name": ['user']},
                            status=status.HTTP_400_BAD_REQUEST)
