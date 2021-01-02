from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.validators import UniqueTogetherValidator

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',
                  'bio', 'role')


class NewUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email',)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=False
    )

    class Meta:
        fields = '__all__'
        exclude_fields = ('title',)
        model = Review
        read_only_fields = ('pub_date',)

    def validate(self, data):
        title = self.context['view'].kwargs.get('title_id')
        author = self.context['request'].user
        message = 'Вы уже оставляли отзыв на данное произведение'
        check_exists = Review.objects.filter(title=title, author=author).exists()
        if check_exists == True:
            raise serializers.ValidationError(message)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        exclude_fields = ('review',)
        model = Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'rating', 'category')
        model = Title


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        fields = '__all__'
        model = Title
