from django.db import models
from django.contrib.auth import get_user_model

from apps.book.models import Book


User = get_user_model()


class Favorite(models.Model):
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )

    def __str__(self):
        return f'{self.user} liked {self.book}'


class Comment(models.Model):
    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    comment = models.CharField(max_length=150, verbose_name='comment')

    def __str__(self) -> str:
        return f'comment from {self.user.username}'


class Rating(models.Model):

    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

    RATING_CHOISES = (
        (ONE, '1'),
        (TWO, '2'),
        (THREE, '3'),
        (FOUR, '4'),
        (FIVE, '5')
    )

    book = models.ForeignKey(
        to=Book,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='ratings'
    )
    rating = models.CharField(max_length=1, choices=RATING_CHOISES)

    def __str__(self) -> str:
        return f'rating from {self.user.username}'