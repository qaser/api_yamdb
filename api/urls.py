from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    GetTokenAPIView, ReviewViewSet, TitleViewSet, UserViewSet,
                    create_new_user)

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
    path(
        'token/',
        GetTokenAPIView.as_view(),
        name='get_token'
    ),
    # path(
    #     'token/refresh/',
    #     TokenRefreshView.as_view(),
    #     name='token_refresh'
    # ),
    path(
        'email/',
        create_new_user,
        name='auth'
    )
]


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/', include(urls_auth))
]
