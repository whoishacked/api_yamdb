from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .mixins import CreateListDestroyViewSet, CreateViewSet
from .permissions import Administrator, OwnerOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitlePostPatchSerializer, TitleSerializer,
                          UserRegSerializer, UserSerializer)


def get_object_or_400(model, **kwargs):
    try:
        instance = model.objects.get(**kwargs)
    except Exception as error:
        raise ParseError(error)
    return instance


class CategoryViewSet(CreateListDestroyViewSet):
    """Categories for titles viewset."""
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (Administrator,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions() 


class GenreViewSet(CreateListDestroyViewSet):
    """Genres viewset."""
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('name',)
    pagination_class = PageNumberPagination
    lookup_field = 'slug'
    permission_classes = (Administrator,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions() 


class TitleViewSet(viewsets.ModelViewSet):
    """Titles viewset."""
    queryset = Title.objects.all().order_by('id')
    serializer_class = TitleSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name', 'year', 'category', 'genre')
    pagination_class = PageNumberPagination
    permission_classes = (Administrator,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitlePostPatchSerializer
        return TitleSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(viewsets.ModelViewSet):
    """User viewset."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    lookup_field = 'username'
    permission_classes = (Administrator,)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if 'role' in request.data:
            return Response(serializer.data,
                            status=status.HTTP_400_BAD_REQUEST)
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user,
                data=request.data,
                partial=True)

            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Reviews viewset."""
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          OwnerOrReadOnly)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        queryset = title.reviews.all().order_by('id')
        return queryset

    def create(self, request, *args, **kwargs):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        review = Review.objects.filter(author=self.request.user, title=title)
        if review.exists():
            content = {
                'Ошибка:': 'Вы уже оставляли отзыв к данному произведению'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Comments viewset."""
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          OwnerOrReadOnly)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['id'])
        queryset = review.comments.all().order_by('id')
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs['id'])
        serializer.save(author=self.request.user, review=review)


class UserRegViewSet(CreateViewSet):
    """Users register viewset."""
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    lookup_field = 'username'

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        username = data.get('username')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(username=username)
        send_mail(
            subject='Код подтверждения для регистрации на yamdb',
            message=f'Код подтверждения для пользователя {user.username}:'
                    f' {user.confirmation_code}',
            from_email='from@example.com',
            recipient_list=[f'{user.email}'],
            fail_silently=False
        )
        return Response(data, status=status.HTTP_200_OK)


class RegAPIView(views.APIView):
    """Refresh token."""
    def post(self, request):
        username = request.data.get('username', [])
        if not username:
            return Response({"field_name": ['username']},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, username=username)
        confirmation_code = request.data.get('confirmation_code', [])
        if confirmation_code != user.confirmation_code:
            return Response({"field_name": ['confirmation_code']},
                            status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user).access_token
        return Response({"token": str(token)}, status=status.HTTP_200_OK)
