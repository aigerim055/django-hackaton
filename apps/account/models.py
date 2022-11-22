import code
from django.db import models
from django.utils.crypto import get_random_string
# from random import randint
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
# from random import randint

class UserManager(BaseUserManager):
    
    def _create(self, username, phone, password, **extra_fields):
        if not username and phone:
            raise ValueError('User must have username and phone')
        user = self.model(
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_staff', False)
        return self._create(username, phone, password, **extra_fields)

    def create_superuser(self, username, phone, password, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        return self._create(username, phone, password, **extra_fields)


class User(AbstractBaseUser):
    RANDOM_STRING_CHARS = "1234567890"


    username = models.CharField(max_length=50, primary_key=True, unique=True)
    phone = models.CharField(max_length=13)  # , unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=10, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, obj=None):
        return self.is_staff

    def create_activation_code(self):
        code = get_random_string(length=6, allowed_chars=self.RANDOM_STRING_CHARS)
        if User.objects.filter(activation_code=code).exists():
            self.create_activation_code()
        self.activation_code = code
        self.save()

    def __str__(self) -> str:
        return self.username