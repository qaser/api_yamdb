from .pagination import CustomPagination
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, serializers, status
from rest_framework import viewsets
from django.core.mail import send_mail
from rest_framework import permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import ParseError
from rest_framework import filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Genre, Review, Title, User
from .permissions import AdminOrReadOnly, ReviewAndCommentPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitlePostSerializer,
                          UserSerializer, NewUserSerializer)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = CustomPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        ReviewAndCommentPermission
    ]

    def get_title(self):  # DRY function
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title

    def get_queryset(self):
         # извлекаю id тайтла из url'а
         title_id = self.kwargs['title_id']
         title = get_object_or_404(Title, id=title_id)
         queryset = title.reviews.all()
         return self.get_title().reviews.all()

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user, title=self.get_title())
        except IntegrityError:  # exception raised when dublicate key in DB
            raise ParseError(detail='Only one review from unique user')


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = CustomPagination
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        ReviewAndCommentPermission
    ]
    
    def get_review(self):  # DRY function
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title__id=self.kwargs['title_id']
        )
        return review

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_review()
        )


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MixinClass(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    pagination_class = CustomPagination
    permission_classes = [AdminOrReadOnly]


class CategoryViewSet(MixinClass):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MixinClass):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly, AdminOrReadOnly]
    filterset_fields = ['category', 'genre', 'year', 'name']


    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitlePostSerializer


class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        code = request.data.get('confirmation_code')
        if user.confirmation_code == code:
            tokens = self.get_tokens_for_user(user)
            return Response({'massage': tokens})
        return Response({'massage': 'wrong confirmation code'})


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination
    serializer_class = UserSerializer
    lookup_field = 'username' 
