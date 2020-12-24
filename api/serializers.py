from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

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
        model = Review
        read_only_fields = ('pub_date',)
        # validators = [
        #     UniqueTogetherValidator(
        #         queryset=Review.objects.all(),
        #         fields=['title', 'author']
        #     )
        # ]


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


class TitleListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    # represent rating field
    def to_representation(self, instance):
        data = super(TitleListSerializer, self).to_representation(instance)
        title = get_object_or_404(Title, id=instance.id)
        # aggregate вроде как медленно работает, но пока так
        title_rating = title.reviews.aggregate(Avg('score'))
        data['rating'] = title_rating.get('score__avg', 0)
        return data


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
