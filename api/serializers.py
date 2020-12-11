from rest_framework import serializers
# from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Review, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Genre


# class TitleSerializer(serializers.ModelSerializer):
#     class Meta:
#         fields = '__all__'
#         model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'pub_date')
        exclude = ['title']  # исключаю поле 'title'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('id', 'pub_date')
        exclude = ['review']
