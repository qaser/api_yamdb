#from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.conf import settings


#User = get_user_model()


# class UserManager(BaseUserManager):

#   def create_user(self, username, email, password):
#     if not email:
#       raise ValueError('User must have an email address')
#     if not username:
#       raise ValueError('User must have a username')

#     user = self.model(username = username, email = self.normalize_email(email))
#     user.set_password(password)
#     user.save(using = self._db)
#     return user

#   def create_superuser(self, username, email, password):
#     user = self.create_user(username = username, email = email, password = password)
#     user.is_staff = True
#     user.is_admin = True
#     user.is_superuser = True
#     user.save(using = self._db)
#     return user

class User(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    ]
    username = models.CharField(max_length = 30, unique = True)
    email = models.EmailField(max_length = 60, unique = True)
    first_name = models.CharField(max_length = 30, null = True, blank = True)
    last_name = models.CharField(max_length = 30, null = True, blank = True)
    bio = models.TextField()
    is_staff = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(choices=ROLE_CHOICES, default='user', max_length=20)


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название категории объекта',
        max_length=50
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
        max_length=50
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
        max_length=50
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
        null=True
    )
    text = models.TextField('текст отзыва', blank=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
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
        settings.AUTH_USER_MODEL,
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

'''
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
'''