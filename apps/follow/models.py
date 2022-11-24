from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserFollowing(models.Model):
    user = models.ForeignKey(
        to=User,
        related_name='following',
        on_delete=models.CASCADE
    )
    following_user = models.ForeignKey(
        to=User,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','following_user'],  name="unique_followers")
        ]
        ordering = ['-created_at']
        verbose_name = 'Follower'
        verbose_name_plural = 'Followers'


    def __str__(self) -> str:
        return f'{self.user} follows {self.following_user}'