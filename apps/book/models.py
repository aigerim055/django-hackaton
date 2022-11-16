from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from slugify import slugify


User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()
    avatar = models.ImageField(max_length=250, blank=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.first_name) + '_' + slugify(self.last_name)
        # if not self.name:
        #     self.name = str(self.first_name) + ' ' + str(self.last_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    class Meta:
        ordering = ['last_name', 'first_name']
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
    

class Book(models.Model):  
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    description = models.TextField(blank=True) # null=True?
    image_link = models.CharField(max_length=255, blank=True)
    genre = models.ManyToManyField(
        to='Genre',
        related_name='books',
        blank=True
    )
    year_published = models.PositiveSmallIntegerField(blank=True)   
    pages = models.PositiveSmallIntegerField(blank=True)   
    quantity = models.PositiveSmallIntegerField()
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.is_available = self.number_available > 0
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})     # вспомнить для чего / надо ли

    class Meta:
        ordering = ['title']  
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'


class Genre(models.Model):                                       
    genre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)

    def __str__(self) -> str:
        return self.genre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'