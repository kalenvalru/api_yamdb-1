from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (APIGetToken, APISignup, CategoryViewSet, GenreViewSet,
                    TitleViewSet, UsersViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(
    'users',
    UsersViewSet,
    basename='users'
)
router.register(
    r'categories',
    CategoryViewSet,
    basename='categories'
)
router.register(
    r'titles',
    TitleViewSet,
    basename='titles'
)
router.register(
    r'genres',
    GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', APISignup.as_view(), name='signup')
]
