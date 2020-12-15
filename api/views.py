from django.db.models.base import Model
from django.shortcuts import render
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from .models import Review, Comment, Title, Category, Genre
from .pagination import CustomPagination
from .serializers import (
    CommentSerializer,
    ReviewSerializer,
    GenreSerializer,
    CategorySerializer
    )


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # извлекаю id тайтла из url'а
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, id=title_id)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
#        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset


# class CategoryViewSet(ModelViewSet):

# class GenreViewSet(ModelViewSet):

# class TitleViewSet(ModelViewSet):
