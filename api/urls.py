from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from .views import CreateUserAPIView, GetTokenAPIView, UserOwnViewSet
from .views import CommentViewSet, ReviewViewSet, UserViewSet, TitleViewSet, CategoryViewSet, GenreViewSet

router = DefaultRouter()
router.register('titles', TitleViewSet, basename='titles')
router.register('categories', CategoryViewSet, basename='category')
router.register('genres', GenreViewSet, basename='genres')
router.register(r'users', UserViewSet, basename='username')
router.register(r'users/me', UserViewSet, basename='user')
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')
router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', GetTokenAPIView.as_view(), name='get_token'),
    path('v1/auth/email/', CreateUserAPIView.as_view, name='auth')
]