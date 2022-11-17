from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class UserProfile(models.Model):
    user = models.OneToOneField(        # user или username
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    first_name = models.CharField('first name', max_length=20)
    last_name = models.CharField('last name', max_length=40)
    bio = models.TextField(default='', blank=True)

    avatar = models.ImageField(upload_to='media')   #upload_to='media')    #######
    birthday = models.DateField(null=True, blank=True)                         # settings include format   # формат как проверяется, выпдает ли календарь
    phone = models.CharField(max_length=14, null=True)    # проверка на номер телефона
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class ProfileImage(models.Model):
    avatar = models.ImageField(upload_to='media')
    profile = models.ForeignKey(
        to=UserProfile,
        on_delete=models.CASCADE,
        related_name='profile_images'
    )
    avatar = models.ImageField(upload_to='media')