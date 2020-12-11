from django.db.models.base import Model
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Review, Comment, Title
from .pagination import CustomPagination
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        # извлекаю id тайтла из url'а
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
#        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset
