from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.deletion import CASCADE
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=40, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    # is_staff = models.BooleanField(default=False)
    # написать поле роли, не знаю какой тип поля
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        return self


# class Genre(models.Model):


class Title(models.Model):
    pass

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
        auto_now_add=True,
        db_index=True
    )

    class Meta:
#        ordering = ('-pub_date',)
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
