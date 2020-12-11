from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории объекта',
        )
    slug = models.SlugField(
        unique=True,
        verbose_name="Поле slug",
        )

    class Meta:
        ordering = ('slug',)


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        )
    slug = models.SlugField(
        unique=True,
        verbose_name="Поле slug",
        )

    class Meta:
        ordering = ('slug',)


class Title(models.Model):
    id = models.AutoField(
        verbose_name='ID произведения',
        primary_key=True,
        )
    name = models.CharField(
        verbose_name='Название',
        )
    year = models.IntegerField(
        verbose_name='Год выпуска',
        )
    rating = models.IntegerField(
        verbose_name='Рейтинг на основе отзывов, если отзывов — `None`',
        null=True,
        blank=True,
        )
    description = models.TextField(
        verbose_name='Описание',
        )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
        related_name='genres',
        blank=True,
        )
    category = models.ForeignKey(
        Category,
        verbose_name='Slug категории',
        on_delete=models.SET_NULL,
        related_name='categories',
        null=True,
        blank=True
        )

    class Meta:
        ordering = ('id',)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=CASCADE,
        verbose_name='произведение',
        related_name='reviews',
        null=True,
        blank=True
    )
    text = models.TextField('текст отзыва', blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='username пользователя',
        related_name='review_author'
    )
    score = models.IntegerField(
        'оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        unique_together = ['author', 'title']


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=CASCADE,
        verbose_name='отзыв',
        related_name='comments',
        null=True,
        blank=True
    )
    text = models.TextField('текст отзыва', blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='username автора комментария',
        related_name='comment_author'
    )
    pub_date = models.DateTimeField(
        'дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
