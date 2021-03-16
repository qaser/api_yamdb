from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, create_new_user,
                    get_token)

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genres')
router.register('users', UserViewSet, basename='users')
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

urls_auth = [
    path('token/', get_token, name='get_token'),
    path('email/', create_new_user, name='email')
]

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urls_auth))
]
