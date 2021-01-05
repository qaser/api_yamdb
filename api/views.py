from django.utils import timezone
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import update_last_login
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from .filters import TitleFilter
from .models import Category, Genre, Review, Title, User
from .permissions import (AdminOrReadOnly, AdminPermission,
                          IsAuthorModeratorAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, NewUserSerializer, ReviewSerializer,
                          TitleListSerializer, TitlePostSerializer,
                          UserSerializer)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnly
    ]

    def get_title(self):  # DRY function for extract 'id' from url and check
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticatedOrReadOnly,
        IsAuthorModeratorAdminOrReadOnly
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


class MixinClass(mixins.ListModelMixin, mixins.CreateModelMixin,
                 mixins.DestroyModelMixin, viewsets.GenericViewSet):
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name']
    lookup_field = 'slug'
    permission_classes = [AdminOrReadOnly, IsAuthenticatedOrReadOnly]


class CategoryViewSet(MixinClass):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(MixinClass):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('id')
    filterset_class = TitleFilter
    permission_classes = [IsAuthenticatedOrReadOnly, AdminOrReadOnly]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleListSerializer
        return TitlePostSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [AdminPermission]
    serializer_class = UserSerializer
    lookup_field = 'username'

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@csrf_exempt
@api_view(['POST'])
# @permission_classes(AllowAny)
def create_new_user(request):
    serializer = NewUserSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    email = request.POST.get('email')
    # нижнее подчёркивание это "мусорный" аргумент, он не учитывается
    # иначе отдаёт кортеж
    user,  _ = User.objects.get_or_create(email=email)
    code = default_token_generator.make_token(user)
    send_mail(
        'Automatic registration',
        f'Dear User! For access to API use this code: {code}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )
    return Response({'email': email})


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@csrf_exempt
@api_view(['POST'])
# @permission_classes(AllowAny)
def get_token(request):
    serializer = NewUserSerializer(data=request.data, many=True)
    serializer.is_valid(raise_exception=True)
    email = request.data.get('email')
    user = get_object_or_404(User, email=email)
    code = request.data.get('confirmation_code')
    check_pass = default_token_generator.check_token(user, code)
    if check_pass:
        tokens = get_tokens_for_user(user)
        return Response({'token': tokens})
    return Response({'message': 'wrong confirmation code'})
