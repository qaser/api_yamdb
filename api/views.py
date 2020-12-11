from django.db.models.base import Model
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Review, Comment
from .pagination import CustomPagination
from .serializers import CommentSerializer, ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination

    def get_object(self):
        queryset = self.get_queryset
        title_id = self.kwargs['title_id']
        return 


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = CustomPagination

    def get_object(self):
        queryset = self.get_queryset
        title_id = self.kwargs['title_id']
        review_id = self.kwargs['review_id']
        return 
