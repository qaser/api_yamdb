from attr import fields
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Review, Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = User


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=False
    )
#    title = serializers.SlugRelatedField(
#        read_only=True,
#        slug_field='description',
#        many=False
#    )

    class Meta:
        fields = '__all__'
#        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review
        read_only_fields = ('id', 'pub_date')
        exclude = ['title']  # исключаю поле 'title'
#        validators =  [
#            UniqueTogetherValidator(
#                queryset=Review.objects.all(),
#                fields=['author', 'title']
#            )
#        ]


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'pub_date')
#        exclude = ['review']


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