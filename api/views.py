from django.db import IntegrityError
from django.db.models import Avg
from django.db.models.base import Model
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Category, Comment, Genre, Review, Title, User
from .pagination import CustomPagination
from .permissions import (AdminOrReadOnly,  # ReviewCommentPermission
                          AdminPermission, IsAuthorOrReadOnlyPermission)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleListSerializer, TitlePostSerializer,
                          UserSerializer)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
#    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly] # ReviewCommentPermission)

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
#    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly] # ReviewCommentPermission)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        get_object_or_404(Title, id=title_id)  # check Title exist
        review_id = self.kwargs['review_id']
        review = get_object_or_404(Review, id=review_id)
        queryset = review.comments.all()
        return queryset

class CreateUserAPIView(APIView):
    permission_classes = (AllowAny,)
 
    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleListSerializer
#    pagination_class = CustomPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'genre', 'year', 'name']

    def get_serializer_class(self):
        if self.action in ('list','retrieve'):
            return TitleListSerializer
        return TitlePostSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
#    permission_classes = [AdminOrReadOnly,]
    filter_backends = [SearchFilter]
#    pagination_class = CustomPagination
    search_fields = ['name', ]
    lookup_field = 'slug'


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
#    pagination_class = CustomPagination
    filter_backends = [SearchFilter]
    filterset_fields = ['name', ]
    lookup_field = 'slug'


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_permissions(self):
        if self.action in ['get', 'patch', 'delete']:
           permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AdminPermission]
        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get', 'patch', 'delete'])
    def get(self, request):
        user_email = request.user.email
        user = get_object_or_404(User, email=user_email)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def patch(self, request):
        user_email = request.user.email
        user = get_object_or_404(User, email=user_email)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class GetTokenAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        email = request.data.get('email')
        user = get_object_or_404(User, email=email)
        code = request.data.get('confirmation_code')
        if user.auth_code == code:
            tokens = get_tokens_for_user(user)
            return Response({'massage': tokens})
        return Response({'massage': 'wrong confirmation code'})
