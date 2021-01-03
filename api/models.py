from datetime import datetime as dt

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE

from . import utils

current_year = dt.now().year


class Role(models.TextChoices):
    ADMIN = 'admin'
    USER = 'user'
    MODERATOR = 'moderator'


class User(AbstractUser):
    username = models.CharField(
        'логин',
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )
    email = models.EmailField(
        'адрес почты',
        max_length=200,
        unique=True
    )
    first_name = models.CharField(
        'имя пользователя',
        max_length=30,
        null=True,
        blank=True
    )
    last_name = models.CharField(
        'фамилия пользователя',
        max_length=30,
        null=True,
        blank=True
    )
    bio = models.TextField('биография', blank=True, null=True)
    date_joined = models.DateTimeField(
        'дата регистрации',
        auto_now_add=True
    )
    role = models.CharField(
        'роль пользователя',
        max_length=30,
        choices=Role.choices,
        default=Role.USER
    )
    confirmation_code = models.CharField(max_length=20)

    class Meta:
        ordering = ('email',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return self.email

    @property
    def is_admin(self):
        return self.is_superuser or self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.is_admin or self.role == Role.MODERATOR


class Category(models.Model):
    name = models.CharField('название категории', max_length=50)
    slug = models.SlugField(
        unique=True,
        verbose_name='путь',
        max_length=100
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='название жанра',
        max_length=50
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='путь',
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'жанр'
        verbose_name_plural = 'жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='название',
        db_index=True,
        max_length=50
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='год выпуска',
        db_index=True,
        validators=[utils.MaxValueValidator(current_year+1)]
    )
    description = models.TextField(
        verbose_name='описание',
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name='жанр',
        blank=True,
        db_index=True,
        related_name='title'
    )
    category = models.ForeignKey(
        Category,
        verbose_name='категория',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
        related_name='title'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'произведение'
        verbose_name_plural = 'произведения'

    def __str__(self):
        return self.name


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
        validators=[utils.MinValueValidator(1), utils.MaxValueValidator(10)]
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
        if len(self.text) > 30:
            return self.text + '...'
        return self.text


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
        if len(self.text) > 30:
            return self.text + '...'
        return self.text
