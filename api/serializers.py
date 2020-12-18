from attr import fields
from django.db.models import Avg
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Comment, Review, Category, Genre, Title, User


class UserSerializer(serializers.ModelSerializer):
 
    date_joined = serializers.ReadOnlyField()
 
    class Meta(object):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name',
                  'date_joined', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        many=False
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('id', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment
        read_only_fields = ('id', 'pub_date')


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        sett = Review.objects.filter(id=instance.id)
        title_score = sett.aggregate(Avg('score'))
        representation['rating'] = title_score.get('score__avg', 0)
        return representation
