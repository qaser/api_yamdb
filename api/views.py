from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from .models import Review, Comment


class ReviewViewSet(ModelViewSet):
    pass


class CommentViewSet(ModelViewSet):
    pass
