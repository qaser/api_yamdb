from rest_framework.routers import DefaultRouter
from django.urls import include, path

from .views import CommentViewSet, ReviewViewSet

router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='reviews')
router.register(r'reviews/(?P<reviews_id>\d+)/comments', CommentViewSet, basename='comments')


urlpatterns = [
    path('v1/', include(router.urls)),
]