from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.deletion import CASCADE

User = get_user_model()

class Review(models.Model):
    text = models.TextField('текст отзыва', blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='username пользователя'
    )
    score = models.IntegerField('оценка', blank=False, null=False)
    pub_date = models.DateTimeField(
        'дата публикации отзыва',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)


class Comment(models.Model):
    text = models.TextField('текст отзыва', blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=CASCADE,
        verbose_name='username автора комментария'
    )
    pub_date = models.DateTimeField(
        'дата публикации комментария',
        auto_now_add=True
    )

    class Meta:
        ordering = ('-pub_date',)
