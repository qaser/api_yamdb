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

from .models import Category, Comment, Genre, Review, Title, User
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission, AdminOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer, TitleListSerializer,
                          GenreSerializer, ReviewSerializer, TitlePostSerializer, UserSerializer)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = CustomPagination


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


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#    permission_classes = [AdminOrReadOnly,]
    filter_backends = [SearchFilter]
    pagination_class = CustomPagination
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    filterset_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
#    queryset = Title.objects.all()
    queryset = Title.objects.annotate(avg_rating=Avg('reviews__score'))
    serializer_class = TitleListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
#    filterset_class = TitleFilter
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'year', 'name']

    def get_serializer_class(self):
        if self.action in ('list','retrieve'):
            return TitleListSerializer
        return TitlePostSerializer

