from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import (CategoryViewSet, GenreViewSet, SignUpViewSet, TitleViewSet,
                    TokenViewSet, UsersViewSet, ReviewViewSet, CommentViewSet)

app_name = 'api'

router = SimpleRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register('users', UsersViewSet, basename='users')
router.register('categories', CategoryViewSet, basename='categories')
router.register('titles', TitleViewSet, basename='titles')
router.register('genres', GenreViewSet, basename='genres')


auth_urls = [
    path(
        'signup/', SignUpViewSet.as_view(), name='signup',
    ),
    path(
        'token/', TokenViewSet.as_view(), name='token'
    )
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(auth_urls)),
]
