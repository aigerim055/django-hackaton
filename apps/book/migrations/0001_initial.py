# Generated by Django 4.1.3 on 2022-11-17 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('about', models.TextField()),
                ('avatar', models.ImageField(upload_to='author_images')),
                ('slug', models.SlugField(blank=True, max_length=120, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name': 'Автор',
                'verbose_name_plural': 'Авторы',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('genre', models.CharField(max_length=30, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=35, primary_key=True, serialize=False)),
                ('parent_genre', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subgenres', to='book.genre', verbose_name='Родительский жанр')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('title', models.CharField(max_length=150, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=200, primary_key=True, serialize=False)),
                ('description', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(upload_to='books_images')),
                ('price', models.DecimalField(decimal_places=2, max_digits=7)),
                ('year_published', models.PositiveSmallIntegerField(blank=True)),
                ('pages', models.PositiveSmallIntegerField(blank=True, default=0)),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
                ('views_count', models.IntegerField(default=0)),
                ('in_stock', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='books', to='book.author')),
                ('genre', models.ManyToManyField(blank=True, related_name='books', to='book.genre')),
            ],
            options={
                'verbose_name': 'Произведение',
                'verbose_name_plural': 'Произведения',
                'ordering': ['title'],
            },
        ),
    ]
