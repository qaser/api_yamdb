from attr import fields
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
#    role = serializers.CharField(max_length=100, source='user_data.role', required=False,)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'bio', 'role')
#        extra_kwargs = {'password': {'write_only': True}}


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=False
    )

    class Meta:
        fields = '__all__'
#        fields = ('id', 'title','text', 'author', 'score', 'pub_date')
        model = Review
#        read_only_fields = ('pub_date',)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
         fields = ('name', 'slug')
         model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
         fields = ('name', 'slug')
         model = Genre


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
#        many=True,
#        read_only=True,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all()
    )

    class Meta:
         fields = '__all__'
         model = Title


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)

    class Meta:
         fields = '__all__'
         model = Title

    # represent rating field
    def to_representation(self, instance):
        title = get_object_or_404(Title, id=instance.id)
        review = title.reviews.all()
        title_rating = review.aggregate(rating=Avg('score'))
        return title_rating
