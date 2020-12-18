from django.db.models.base import Model
from django.db.models import Avg
from django.db import IntegrityError
from django.http import response
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ParseError
from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment, Review, Title, User
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission, AdminOrReadOnly
from .serializers import (CommentSerializer, ReviewSerializer)

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
#    permission_classes = (IsAuthenticatedOrReadOnly)

    def get_queryset(self):
         # извлекаю id тайтла из url'а
         title_id = self.kwargs['title_id']
         title = get_object_or_404(Title, id=title_id)
         queryset = title.reviews.all()
         return queryset
#        return Review.objects.filter(title=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        title_id = self.kwargs['title_id']
        title = get_object_or_404(Title, id=title_id)
        try:
            serializer.save(author=self.request.user, title=title)
        except IntegrityError:  # exception raised when dublicate key in DB
            raise ParseError(detail='Only one review from unique user')  # code=None?


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
#    permission_classes = (IsAuthenticatedOrReadOnly)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)  # check Title exist
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

'''
class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'year', 'name']

    def get_serializer_class(self):
        if self.action in ('list','retrieve'):
            return TitleListSerializer
        return TitlePostSerializer

'''