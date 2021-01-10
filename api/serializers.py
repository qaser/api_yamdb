from rest_framework import serializers

from .models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name',
            'username', 'email',
            'bio', 'role',
        )


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
        exclude = ('title',)
        model = Review
        read_only_fields = ('pub_date',)

    def validate(self, data):
        request_context = self.context['request']
        request_method = request_context.method
        if request_method != 'POST':
            return data
        title = request_context.parser_context['kwargs']['title_id']
        author = request_context.user
        message = 'Вы уже оставляли отзыв на данное произведение'
        check_exists = (
            Review.objects.filter(title=title, author=author).exists()
        )
        if check_exists:
            raise serializers.ValidationError(message)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        exclude = ('review',)
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
        fields = '__all__'
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
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title

    def to_representation(self, instance):
        return TitleListSerializer(instance).data
