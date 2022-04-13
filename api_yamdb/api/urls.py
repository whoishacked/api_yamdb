from rest_framework_simplejwt.views import TokenObtainPairView
from django.urls import include, path
from rest_framework import routers

from .views import TitleViewSet, CategoryViewSet, GenreViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain'),
]
