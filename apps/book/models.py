from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify


User = get_user_model()


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    about = models.TextField()
    avatar = models.ImageField(upload_to='author_images')
    slug = models.SlugField(primary_key=True, blank=True, max_length=120)
    name = models.CharField(max_length=100, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.last_name) + '_' + slugify(self.first_name)
        if not self.name:
            self.name = str(self.last_name) + ' ' + str(self.first_name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.first_name} {self.last_name}' 

    class Meta:
        ordering = ['name']
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'
    

class Book(models.Model):  
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=200, primary_key=True, blank=True)
    author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='books'
    )
    description = models.TextField(blank=True, null=True) # null=True?
    image = models.ImageField(upload_to='books_images')
    genre = models.ManyToManyField(
        to='Genre',
        related_name='books',
        blank=True
    )
    price = models.DecimalField(max_digits=7, decimal_places=2)
    year_published = models.PositiveSmallIntegerField(blank=True)   
    pages = models.PositiveSmallIntegerField(blank=True, default=0)   
    quantity = models.PositiveSmallIntegerField(default=0)
    views_count = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        self.in_stock = self.quantity > 0
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ['title']  
        verbose_name = 'Book'
        verbose_name_plural = 'Books'


class Genre(models.Model):                                       
    genre = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(primary_key=True, blank=True, max_length=35)
    parent_genre = models.ForeignKey(
        verbose_name='Parent genre',
        to='self', 
        on_delete=models.CASCADE, 
        related_name='subgenres',
        blank=True,
        null=True
        )

    def __str__(self) -> str:
        return self.genre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.genre)
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'