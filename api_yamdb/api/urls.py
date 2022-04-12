from rest_framework_simplejwt.views import TokenObtainPairView

from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet


app_name = 'api'

router = routers.DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path(
        'v1/auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain'),
    path('v1/', include(router.urls)),
]
