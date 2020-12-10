from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()

class Review(models.Model):
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='имя пользователя'
    )
    score = models.IntegerField('оценка')
    pub_date = models.DateTimeField(
        'дата публикации отзыва',
        auto_now_add=True
    )


class Comment(models.Model):
#    id = models.IntegerField('ID комментария')
    text = models.TextField('текст отзыва')
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='имя автора комментария'
    )
    pub_date = models.DateTimeField(
        'дата публикации комментария',
        auto_now_add=True
    )