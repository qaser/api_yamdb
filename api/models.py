from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import BaseValidator, MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.utils.deconstruct import deconstructible
from datetime import datetime as dt

current_year = dt.now().year

@deconstructible
class MaxValueValidator(BaseValidator):
    message = ('Значение должно быть не выше 10-ти')
    code = 'max_value'

    def compare(self, a, b):
        return a > b


@deconstructible
class MinValueValidator(BaseValidator):
    message = ('Значение должно быть не ниже единицы')
    code = 'min_value'

    def compare(self, a, b):
        return a < b


class Role(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'


class User(AbstractUser):
    username = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(max_length=60, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(max_length=20)


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории объекта',
        max_length=50
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Поле slug',
        max_length=100
    )

    class Meta:
        ordering = ('slug',)


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Название жанра',
        max_length=50
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Поле slug',
    )

    class Meta:
        ordering = ('slug',)


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50
    )
    year = models.PositiveIntegerField(
        verbose_name='Год выпуска',
        db_index=True,
        validators=[MaxValueValidator(current_year+1)]
        )
    description = models.TextField(
        verbose_name='Описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='Slug жанра',
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
        null=True
    )
    text = models.TextField('текст отзыва', blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name='автор отзыва',
        related_name='review_author'
    )
    score = models.PositiveSmallIntegerField(
        'оценка',
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'дата публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            )
        ]

    def __str__(self):
        return f'Отзыв на произведение {self.title}. Автор: {self.author}.'


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=CASCADE,
        verbose_name='отзыв',
        related_name='comments',
        null=True,
        blank=True
    )
    text = models.TextField('текст комментария', blank=False, null=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=CASCADE,
        verbose_name='автор комментария',
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'

    def __str__(self):
        return f'Комментарий пользователя {self.author} к отзыву {self.review}'
